// Integrantes:
// Dafne
// Santiago

#include <msp430.h>

unsigned char mensaje[] = {"#.###,#.###\n"};
unsigned char i;

unsigned int ADC_result[2];
unsigned long j;

#pragma vector = TIMER0_A0_VECTOR
__interrupt void Timer_A(void)
{
    TA0CCR0 += 10000;                    // Interrupciones cada 1ms

    ADC10CTL0 &= ~ENC;
    ADC10SA = (unsigned int)&ADC_result; // Configurar destino de datos del ADC
    ADC10CTL0 |= ENC + ADC10SC;          // Encender ADC y empezar conversión
}

#pragma vector = ADC10_VECTOR
__interrupt void ADC10_ISR(void)
{
    ADC_result[1] = ((unsigned long)ADC_result[1] * 3300) / 1023;

    mensaje[4] = (ADC_result[1] % 10) + '0';
    ADC_result[1] /= 10;
    mensaje[3] = (ADC_result[1] % 10) + '0';
    ADC_result[1] /= 10;
    mensaje[2] = (ADC_result[1] % 10) + '0';
    ADC_result[1] /= 10;
    mensaje[0] = (ADC_result[1] % 10) + '0';
    ADC_result[1] /= 10;

    ADC_result[0] = ((unsigned long)ADC_result[0] * 3300) / 1023;

    mensaje[10] = (ADC_result[0] % 10) + '0';
    ADC_result[0] /= 10;
    mensaje[9] = (ADC_result[0] % 10) + '0';
    ADC_result[0] /= 10;
    mensaje[8] = (ADC_result[0] % 10) + '0';
    ADC_result[0] /= 10;
    mensaje[6] = (ADC_result[0] % 10) + '0';
    ADC_result[0] /= 10;

    IE2 |= UCA0TXIE;
}

#pragma vector = USCIAB0TX_VECTOR
__interrupt void UART0_ISR(void)
{
    if(mensaje[i] != '\0')
    {
        while(!(IFG2 & UCA0TXIFG));
        UCA0TXBUF = mensaje[i++];
        for(j = 0; j < 5000; j++);
    }
    else
    {
        IE2 &= ~UCA0TXIE;
        i = 0;
    }
}

int main(void)
{
    WDTCTL = WDTPW | WDTHOLD;                                   // Stop watchdog timer

    // Timer A1 configuration
    TA0CTL = TASSEL_2 + MC_2;                                   // TASSEL_2: SMCLK / MC_2: Continuos mode
    TA0CCTL0 = CCIE;
    TA0CCR0 = TAR + 10000;

    // ADC configuration
    ADC10CTL1 = INCH_4 + CONSEQ_1;                              // A4/A3/A2/A1, single sequence
    ADC10CTL0 = SREF_0 + ADC10SHT_2 + MSC + ADC10ON + ADC10IE;
    ADC10DTC1 = 2;                                              // 2 conversions
    ADC10AE0 |= BIT4 + BIT3;                                    // P1.4,3 ADC10 option select      // Seleccionar A4 como canal más alto / Modo Secuencia Canales

    // Configurar UART
    P1SEL=BIT2+BIT1;
    UCA0CTL1=UCSSEL_2;                                          // Select SMCLK as UART clock (1 MHz)
    UCA0BR0 = 104;
    P1SEL2=BIT2+BIT1;

    __bis_SR_register(GIE);                                     // Global Enable interrupt

    while(1)
    {
    }
}
