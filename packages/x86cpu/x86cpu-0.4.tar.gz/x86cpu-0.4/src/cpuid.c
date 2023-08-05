/*
 * Using the cpuid instruction to get CPU information
 *
 * See: https://en.wikipedia.org/wiki/CPUID
 */

#include <string.h>

#include "cpuid.h"

int has_cpuid(void)
{
#if defined(__x86_64__) || defined(_M_AMD64) || defined (_M_X64)
    /* All 64-bit capable chips have cpuid, according to
     * https://software.intel.com/en-us/articles/using-cpuid-to-detect-the-presence-of-sse-41-and-sse-42-instruction-sets/
     */
    return 1;
#else
    /*
     * cpuid instruction present if it is possible to set the ID bit in EFLAGS.
     * ID bit is 0x200000 (21st bit).
     *
     * https://software.intel.com/en-us/articles/using-cpuid-to-detect-the-presence-of-sse-41-and-sse-42-instruction-sets/
     * http://wiki.osdev.org/CPUID
     */
    int tf = 0;
#if defined (_MSC_VER)
    /*
     * See also comments in for gcc asm below.
     * Notes on MSVX asm and registers at
     * https://msdn.microsoft.com/en-us/library/k1a8ss06.aspx
     */
    __asm {
        push ecx;  just in case (__fastcall needs ecx preserved)
        pushfd;  original eflags
        pushfd;  original eflags again
        pop eax;  copy of eflags into eax
        mov ecx, eax;  store original eflags in ecx
        xor eax, 200000h;  flip bit 21
        push eax;  set eflags from eax
        popfd;  this call will unflip bit 21 if we lack cpuid
        pushfd;  copy of new eflags into eax
        pop eax
        xor eax, ecx;  check whether copy of eflags still has flipped bit
        shr eax, 21;   1 if bit still flipped, 0 otherwise
        mov tf, eax;  put eax result into return variable
        popfd  ; restore original eflags
        pop ecx ; restore original ecx
    }
#else
    __asm__ __volatile__(
        "pushfl; pop %%eax;"  /* get current eflags into eax */
        "mov %%eax, %%ecx;"  /* store copy of input eflags in ecx */
        "xorl $0x200000, %%eax;"  /* flip bit 21 */
        "push %%eax; popfl;"  /* try to set eflags with this bit flipped */
        "pushfl; pop %%eax;"  /* get resulting eflags back into eax */
        "xorl %%ecx, %%eax;"  /* is bit still flipped cf original? */
        "shrl $21, %%eax;"   /* if so, we have cpuid */
        : "=a" (tf)  /* outputs */
        :            /* inputs */
        : "cc", "%ecx");     /* eflags and ecx are clobbered */
#endif
    return tf;
#endif
}

/* shift a by b bits to the right, then mask with c */
#define SHIFT_MASK(a, b, c) ((((a) >> (b)) & (c)))

/*
 * https://software.intel.com/en-us/articles/using-cpuid-to-detect-the-presence-of-sse-41-and-sse-42-instruction-sets/
 * https://software.intel.com/en-us/articles/how-to-detect-new-instruction-support-in-the-4th-generation-intel-core-processor-family
 * https://en.wikipedia.org/wiki/CPUID#CPUID_usage_from_high-level_languages
 */
void read_cpuid(uint32_t op, uint32_t sub_op, e_registers_t* reg)
{
#if defined(_MSC_VER)
    int cpu_info[4] = {-1};
    __cpuidex(cpu_info, (int)op, (int)sub_op);
    reg->eax = cpu_info[0];
    reg->ebx = cpu_info[1];
    reg->ecx = cpu_info[2];
    reg->edx = cpu_info[3];
#else
    /*
     * Wikipedia page suggests it is necessary to stash ebx register on 32-bit,
     * rbx register on 64-bit:
     * https://en.wikipedia.org/wiki/CPUID#CPUID_usage_from_high-level_languages
     *
     * However, experiments with
     * $ gcc -fverbose-asm -g -c cpuid.c
     * $ objdump -S -d cpuid.o > cpuid.s
     * showed that gcc stashes these by default.
     */
    __asm__ __volatile__(
        "cpuid;"
        : "=a" (reg->eax), "=b" (reg->ebx), "=c" (reg->ecx), "=d" (reg->edx)
        : "a" (op), "c" (sub_op)
        : "cc");
#endif
}

void read_vendor_string(e_registers_t cpuid_1, char* vendor)
{
    /* Read vendor string from ebx, edx, ecx
     * Registers in `cpuid_1` resulted from call to read_cpuid(1, 0, &cpuid_1)
     */
    uint32_t* char_as_int=(uint32_t*)vendor;
    *(char_as_int++) = cpuid_1.ebx;
    *(char_as_int++) = cpuid_1.edx;
    *(char_as_int) = cpuid_1.ecx;
    vendor[12] = '\0';
}

void read_brand_string(char* brand)
{
    /*
     * https://en.wikipedia.org/wiki/CPUID#EAX.3D80000002h.2C80000003h.2C80000004h:_Processor_Brand_String
     */
    uint32_t* char_as_int=(uint32_t*)brand;
    int op;
    e_registers_t registers;
    /* does this cpuid support extended calls up to 0x80000004? */
    read_cpuid(0x80000000, 0, &registers);
    if (registers.eax < 0x80000004)
    {
        brand[0] = '\0';
    }
    for (op = 0x80000002; op < 0x80000005; op++)
    {
        read_cpuid(op, 0, &registers);
        *(char_as_int++) = registers.eax;
        *(char_as_int++) = registers.ebx;
        *(char_as_int++) = registers.ecx;
        *(char_as_int++) = registers.edx;
    }
}

void read_classifiers(e_registers_t cpuid_1, cpu_classifiers_t* cpu_params)
{
    /*
    * 3:0 – Stepping
    * 7:4 – Model
    * 11:8 – Family
    * 13:12 – Processor Type
    * 19:16 – Extended Model
    * 27:20 – Extended Family
    * See:
    * https://en.wikipedia.org/wiki/CPUID#EAX.3D1:_Processor_Info_and_Feature_Bits
    * Page 3-191 of
    * http://www.intel.com/content/www/us/en/architecture-and-technology/64-ia-32-architectures-software-developer-vol-2a-manual.html
    */
    uint32_t eax = cpuid_1.eax;
    cpu_params->stepping = SHIFT_MASK(eax, 0, 0x0f);
    cpu_params->model = SHIFT_MASK(eax,  4, 0x0f);
    cpu_params->family = SHIFT_MASK(eax, 8, 0x0f);
    cpu_params->processor_type = SHIFT_MASK(eax, 12, 0x03);
    cpu_params->extended_model = SHIFT_MASK(eax, 16, 0x0f);
    cpu_params->extended_family = SHIFT_MASK(eax, 20, 0xff);
}

int os_supports_avx(e_registers_t cpuid_1)
{
    /*
     * The cpuid(1) ECX register tells us if the CPU supports AVX.
     *
     * For the OS to support AVX, it needs to preserve the AVX YMM registers
     * when doing a context switch.  In order to do this, the needs to support
     * the relevant instructions, and the OS needs to know to preserve these
     * registers.
     *
     * See:
     * https://en.wikipedia.org/wiki/CPUID
     * https://en.wikipedia.org/wiki/Advanced_Vector_Extensions
     * https://software.intel.com/en-us/blogs/2011/04/14/is-avx-enabled/
     */
    uint32_t mask = BIT_MASK(26, 28);
    return ((cpuid_1.ecx & mask) == mask) ? os_restores_ymm() : 0;
}
