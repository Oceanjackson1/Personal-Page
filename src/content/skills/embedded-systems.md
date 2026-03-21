---
title: "Embedded Systems"
description: "Use when developing firmware for microcontrollers, implementing RTOS applications, or optimizing power consumption. Invoke for STM32, ESP32, FreeRTOS, bare-metal, power optimization, real-time systems, configure peripherals, write interrupt handle..."
category: "other"
source: "community"
author: "Community"
tags: ["embedded", "systems"]
date: 2026-03-20
---

# Embedded Systems Engineer

Senior embedded systems engineer with deep expertise in microcontroller programming, RTOS implementation, and hardware-software integration for resource-constrained devices.

## Core Workflow

1. **Analyze constraints** - Identify MCU specs, memory limits, timing requirements, power budget
2. **Design architecture** - Plan task structure, interrupts, peripherals, memory layout
3. **Implement drivers** - Write HAL, peripheral drivers, RTOS integration
4. **Validate implementation** - Compile with `-Wall -Werror`, verify no warnings; run static analysis (e.g. `cppcheck`); confirm correct register bit-field usage against datasheet
5. **Optimize resources** - Minimize code size, RAM usage, power consumption
6. **Test and verify** - Validate timing with logic analyzer or oscilloscope; check stack usage with `uxTaskGetStackHighWaterMark()`; measure ISR latency; confirm no missed deadlines under worst-case load; if issues found, return to step 4

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| RTOS Patterns | `references/rtos-patterns.md` | FreeRTOS tasks, queues, synchronization |
| Microcontroller | `references/microcontroller-programming.md` | Bare-metal, registers, peripherals, interrupts |
| Power Management | `references/power-optimization.md` | Sleep modes, low-power design, battery life |
| Communication | `references/communication-protocols.md` | I2C, SPI, UART, CAN implementation |
| Memory & Performance | `references/memory-optimization.md` | Code size, RAM usage, flash management |

## Constraints

### MUST DO
- Optimize for code size and RAM usage
- Use `volatile` for hardware registers and ISR-shared variables
- Implement proper interrupt handling (short ISRs, defer work to tasks)
- Add watchdog timer for reliability
- Use proper synchronization primitives
- Document resource usage (flash, RAM, power)
- Handle all error conditions
- Consider timing constraints and jitter

### MUST NOT DO
- Use blocking operations in ISRs
- Allocate memory dynamically without bounds checking
- Skip critical section protection
- Ignore hardware errata and limitations
- Use floating-point without hardware support awareness
- Access shared resources without synchronization
- Hardcode hardware-specific values
- Ignore power consumption requirements

## Code Templates

### Minimal ISR Pattern (ARM Cortex-M / STM32 HAL)

```c
/* Flag shared between ISR and task — must be volatile */
static volatile uint8_t g_uart_rx_flag = 0;
static volatile uint8_t g_uart_rx_byte = 0;

/* Keep ISR short: read hardware, set flag, exit */
void USART2_IRQHandler(void) {
    if (USART2->SR & USART_SR_RXNE) {
        g_uart_rx_byte = (uint8_t)(USART2->DR & 0xFF); /* clears RXNE */
        g_uart_rx_flag = 1;
    }
}

/* Main loop or RTOS task processes the flag */
void process_uart(void) {
    if (g_uart_rx_flag) {
        __disable_irq();                   /* enter critical section */
        uint8_t byte = g_uart_rx_byte;
        g_uart_rx_flag = 0;
        __enable_irq();                    /* exit critical section  */
        handle_byte(byte);
    }
}
```

### FreeRTOS Task Creation Skeleton

```c
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"

#define SENSOR_TASK_STACK  256   /* words */
#define SENSOR_TASK_PRIO   2

static QueueHandle_t xSensorQueue;

static void vSensorTask(void *pvParameters) {
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xPeriod  = pdMS_TO_TICKS(10); /* 10 ms period */

    for (;;) {
        /* Periodic, deadline-driven read */
        uint16_t raw = adc_read_channel(ADC_CH0);
        xQueueSend(xSensorQueue, &raw, 0); /* non-blocking send */

        /* Check stack headroom in debug builds */
        configASSERT(uxTaskGetStackHighWaterMark(NULL) > 32);

        vTaskDelayUntil(&xLastWakeTime, xPeriod);
    }
}

void app_init(void) {
    xSensorQueue = xQueueCreate(8, sizeof(uint16_t));
    configASSERT(xSensorQueue != NULL);

    xTaskCreate(vSensorTask, "Sensor", SENSOR_TASK_STACK,
                NULL, SENSOR_TASK_PRIO, NULL);
    vTaskStartScheduler();
}
```

### GPIO + Timer-Interrupt Blink (Bare-Metal STM32)

```c
/* Demonstrates: clock enable, register-level GPIO, TIM2 interrupt */
#include "stm32f4xx.h"

void TIM2_IRQHandler(void) {
    if (TIM2->SR & TIM_SR_UIF) {
        TIM2->SR &= ~TIM_SR_UIF;           /* clear update flag */
        GPIOA->ODR ^= GPIO_ODR_OD5;        /* toggle LED on PA5  */
    }
}

void blink_init(void) {
    /* GPIO */
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    GPIOA->MODER |= GPIO_MODER_MODER5_0;  /* PA5 output */

    /* TIM2 @ ~1 Hz (84 MHz APB1 × 2 = 84 MHz timer clock) */
    RCC->APB1ENR |= RCC_APB1ENR_TIM2EN;
    TIM2->PSC  = 8399;   /* /8400  → 10 kHz  */
    TIM2->ARR  = 9999;   /* /10000 → 1 Hz    */
    TIM2->DIER |= TIM_DIER_UIE;
    TIM2->CR1  |= TIM_CR1_CEN;

    NVIC_SetPriority(TIM2_IRQn, 6);
    NVIC_EnableIRQ(TIM2_IRQn);
}
```

## Output Templates

When implementing embedded features, provide:
1. Hardware initialization code (clocks, peripherals, GPIO)
2. Driver implementation (HAL layer, interrupt handlers)
3. Application code (RTOS tasks or main loop)
4. Resource usage summary (flash, RAM, power estimate)
5. Brief explanation of timing and optimization decisions

---

## Reference: Communication Protocols

# Communication Protocols

## I2C Master Implementation

```c
#include "stm32f4xx.h"

// I2C1 on PB6 (SCL) and PB7 (SDA)
void I2C_Init(void) {
    // Enable clocks
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOBEN;
    RCC->APB1ENR |= RCC_APB1ENR_I2C1EN;

    // Configure GPIO pins (alternate function, open-drain)
    GPIOB->MODER |= (2 << GPIO_MODER_MODER6_Pos) | (2 << GPIO_MODER_MODER7_Pos);
    GPIOB->OTYPER |= GPIO_OTYPER_OT6 | GPIO_OTYPER_OT7;
    GPIOB->OSPEEDR |= (3 << GPIO_OSPEEDR_OSPEEDR6_Pos) | (3 << GPIO_OSPEEDR_OSPEEDR7_Pos);
    GPIOB->PUPDR |= (1 << GPIO_PUPDR_PUPDR6_Pos) | (1 << GPIO_PUPDR_PUPDR7_Pos);
    GPIOB->AFR[0] |= (4 << GPIO_AFRL_AFRL6_Pos) | (4 << GPIO_AFRL_AFRL7_Pos);

    // Reset I2C
    I2C1->CR1 |= I2C_CR1_SWRST;
    I2C1->CR1 &= ~I2C_CR1_SWRST;

    // Configure I2C timing for 100kHz (APB1 = 42MHz)
    I2C1->CR2 = 42;  // FREQ = 42MHz
    I2C1->CCR = 210;  // CCR = 42MHz / (2 * 100kHz) = 210
    I2C1->TRISE = 43; // TRISE = (1000ns / 23.8ns) + 1 = 43

    // Enable I2C
    I2C1->CR1 |= I2C_CR1_PE;
}

// I2C write with timeout
bool I2C_Write(uint8_t addr, uint8_t *data, uint16_t len) {
    uint32_t timeout = 10000;

    // Generate start condition
    I2C1->CR1 |= I2C_CR1_START;
    while (!(I2C1->SR1 & I2C_SR1_SB) && --timeout);
    if (timeout == 0) return false;

    // Send address
    I2C1->DR = (addr << 1);
    timeout = 10000;
    while (!(I2C1->SR1 & I2C_SR1_ADDR) && --timeout);
    if (timeout == 0) return false;

    // Clear ADDR flag
    (void)I2C1->SR1;
    (void)I2C1->SR2;

    // Send data
    for (uint16_t i = 0; i < len; i++) {
        I2C1->DR = data[i];
        timeout = 10000;
        while (!(I2C1->SR1 & I2C_SR1_TXE) && --timeout);
        if (timeout == 0) return false;
    }

    // Wait for BTF
    timeout = 10000;
    while (!(I2C1->SR1 & I2C_SR1_BTF) && --timeout);
    if (timeout == 0) return false;

    // Generate stop condition
    I2C1->CR1 |= I2C_CR1_STOP;

    return true;
}

// I2C read
bool I2C_Read(uint8_t addr, uint8_t *data, uint16_t len) {
    uint32_t timeout = 10000;

    // Generate start
    I2C1->CR1 |= I2C_CR1_START;
    while (!(I2C1->SR1 & I2C_SR1_SB) && --timeout);
    if (timeout == 0) return false;

    // Send address with read bit
    I2C1->DR = (addr << 1) | 1;
    timeout = 10000;
    while (!(I2C1->SR1 & I2C_SR1_ADDR) && --timeout);
    if (timeout == 0) return false;

    // Clear ADDR flag
    (void)I2C1->SR1;
    (void)I2C1->SR2;

    if (len == 1) {
        // Single byte read
        I2C1->CR1 &= ~I2C_CR1_ACK;
        I2C1->CR1 |= I2C_CR1_STOP;

        timeout = 10000;
        while (!(I2C1->SR1 & I2C_SR1_RXNE) && --timeout);
        if (timeout == 0) return false;

        data[0] = I2C1->DR;
    } else {
        // Multiple byte read
        I2C1->CR1 |= I2C_CR1_ACK;

        for (uint16_t i = 0; i < len; i++) {
            if (i == len - 1) {
                I2C1->CR1 &= ~I2C_CR1_ACK;
                I2C1->CR1 |= I2C_CR1_STOP;
            }

            timeout = 10000;
            while (!(I2C1->SR1 & I2C_SR1_RXNE) && --timeout);
            if (timeout == 0) return false;

            data[i] = I2C1->DR;
        }
    }

    return true;
}

// I2C register read (common pattern)
bool I2C_ReadRegister(uint8_t addr, uint8_t reg, uint8_t *data, uint16_t len) {
    if (!I2C_Write(addr, &reg, 1)) return false;
    return I2C_Read(addr, data, len);
}
```

## SPI Master Implementation

```c
// SPI1 on PA5 (SCK), PA6 (MISO), PA7 (MOSI)
void SPI_Init(void) {
    // Enable clocks
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    RCC->APB2ENR |= RCC_APB2ENR_SPI1EN;

    // Configure GPIO pins
    GPIOA->MODER |= (2 << GPIO_MODER_MODER5_Pos) |
                    (2 << GPIO_MODER_MODER6_Pos) |
                    (2 << GPIO_MODER_MODER7_Pos);
    GPIOA->AFR[0] |= (5 << GPIO_AFRL_AFRL5_Pos) |
                     (5 << GPIO_AFRL_AFRL6_Pos) |
                     (5 << GPIO_AFRL_AFRL7_Pos);

    // Configure SPI: Master, 8-bit, MSB first, fPCLK/16 (~5MHz)
    SPI1->CR1 = SPI_CR1_MSTR |        // Master mode
                SPI_CR1_SSM |         // Software slave management
                SPI_CR1_SSI |         // Internal slave select
                (3 << SPI_CR1_BR_Pos) | // Baud rate fPCLK/16
                SPI_CR1_SPE;          // Enable SPI
}

uint8_t SPI_Transfer(uint8_t data) {
    // Wait for TX buffer empty
    while (!(SPI1->SR & SPI_SR_TXE));
    SPI1->DR = data;

    // Wait for RX buffer not empty
    while (!(SPI1->SR & SPI_SR_RXNE));
    return SPI1->DR;
}

void SPI_TransferBuffer(uint8_t *tx_data, uint8_t *rx_data, uint16_t len) {
    for (uint16_t i = 0; i < len; i++) {
        rx_data[i] = SPI_Transfer(tx_data[i]);
    }
}

// SPI with DMA for high-speed transfers
void SPI_DMA_Init(void) {
    RCC->AHB1ENR |= RCC_AHB1ENR_DMA2EN;

    // Configure TX DMA (DMA2 Stream 3 Channel 3)
    DMA2_Stream3->CR = 0;
    while (DMA2_Stream3->CR & DMA_SxCR_EN);

    DMA2_Stream3->PAR = (uint32_t)&(SPI1->DR);
    DMA2_Stream3->CR = (3 << DMA_SxCR_CHSEL_Pos) |  // Channel 3
                       (0 << DMA_SxCR_MSIZE_Pos) |  // 8-bit memory
                       (0 << DMA_SxCR_PSIZE_Pos) |  // 8-bit peripheral
                       DMA_SxCR_MINC |               // Memory increment
                       DMA_SxCR_DIR_0;               // Memory to peripheral

    // Configure RX DMA (DMA2 Stream 0 Channel 3)
    DMA2_Stream0->CR = 0;
    while (DMA2_Stream0->CR & DMA_SxCR_EN);

    DMA2_Stream0->PAR = (uint32_t)&(SPI1->DR);
    DMA2_Stream0->CR = (3 << DMA_SxCR_CHSEL_Pos) |
                       (0 << DMA_SxCR_MSIZE_Pos) |
                       (0 << DMA_SxCR_PSIZE_Pos) |
                       DMA_SxCR_MINC;

    // Enable SPI DMA requests
    SPI1->CR2 |= SPI_CR2_TXDMAEN | SPI_CR2_RXDMAEN;
}

bool SPI_DMA_Transfer(uint8_t *tx_data, uint8_t *rx_data, uint16_t len) {
    // Configure DMA streams
    DMA2_Stream3->M0AR = (uint32_t)tx_data;
    DMA2_Stream3->NDTR = len;
    DMA2_Stream0->M0AR = (uint32_t)rx_data;
    DMA2_Stream0->NDTR = len;

    // Enable DMA streams
    DMA2_Stream0->CR |= DMA_SxCR_EN;
    DMA2_Stream3->CR |= DMA_SxCR_EN;

    // Wait for transfer complete
    uint32_t timeout = 100000;
    while ((DMA2_Stream0->CR & DMA_SxCR_EN) && --timeout);
    while ((DMA2_Stream3->CR & DMA_SxCR_EN) && --timeout);

    return timeout > 0;
}
```

## UART with Interrupt and Circular Buffer

```c
#define UART_RX_BUFFER_SIZE 256

typedef struct {
    uint8_t buffer[UART_RX_BUFFER_SIZE];
    uint16_t head;
    uint16_t tail;
} UARTBuffer_t;

volatile UARTBuffer_t uart_rx_buffer = {0};

void UART_Init_IRQ(void) {
    // Enable clocks
    RCC->APB1ENR |= RCC_APB1ENR_USART2EN;
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;

    // Configure GPIO
    GPIOA->MODER |= (2 << GPIO_MODER_MODER2_Pos) | (2 << GPIO_MODER_MODER3_Pos);
    GPIOA->AFR[0] |= (7 << GPIO_AFRL_AFRL2_Pos) | (7 << GPIO_AFRL_AFRL3_Pos);

    // Configure USART
    USART2->BRR = 0x2D9;  // 115200 baud
    USART2->CR1 = USART_CR1_TE | USART_CR1_RE | USART_CR1_RXNEIE | USART_CR1_UE;

    // Enable NVIC
    NVIC_SetPriority(USART2_IRQn, 2);
    NVIC_EnableIRQ(USART2_IRQn);
}

void USART2_IRQHandler(void) {
    if (USART2->SR & USART_SR_RXNE) {
        uint8_t data = USART2->DR;

        uint16_t next_head = (uart_rx_buffer.head + 1) % UART_RX_BUFFER_SIZE;

        if (next_head != uart_rx_buffer.tail) {
            uart_rx_buffer.buffer[uart_rx_buffer.head] = data;
            uart_rx_buffer.head = next_head;
        }
        // Else: buffer overflow, discard data
    }

    if (USART2->SR & USART_SR_ORE) {
        // Clear overrun error
        (void)USART2->DR;
    }
}

uint16_t UART_Available(void) {
    return (uart_rx_buffer.head - uart_rx_buffer.tail + UART_RX_BUFFER_SIZE) % UART_RX_BUFFER_SIZE;
}

bool UART_ReadByte(uint8_t *data) {
    if (uart_rx_buffer.head == uart_rx_buffer.tail) {
        return false;  // Buffer empty
    }

    *data = uart_rx_buffer.buffer[uart_rx_buffer.tail];
    uart_rx_buffer.tail = (uart_rx_buffer.tail + 1) % UART_RX_BUFFER_SIZE;

    return true;
}

uint16_t UART_ReadBuffer(uint8_t *buffer, uint16_t max_len) {
    uint16_t count = 0;

    while (count < max_len && UART_ReadByte(&buffer[count])) {
        count++;
    }

    return count;
}
```

## CAN Bus Implementation

```c
// CAN on PB8 (RX) and PB9 (TX)
void CAN_Init(void) {
    // Enable clocks
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOBEN;
    RCC->APB1ENR |= RCC_APB1ENR_CAN1EN;

    // Configure GPIO
    GPIOB->MODER |= (2 << GPIO_MODER_MODER8_Pos) | (2 << GPIO_MODER_MODER9_Pos);
    GPIOB->AFR[1] |= (9 << GPIO_AFRH_AFRH0_Pos) | (9 << GPIO_AFRH_AFRH1_Pos);

    // Enter initialization mode
    CAN1->MCR |= CAN_MCR_INRQ;
    while (!(CAN1->MSR & CAN_MSR_INAK));

    // Configure timing: 500kbps (APB1 = 42MHz)
    // BRP=6, TS1=13, TS2=2 -> 42MHz/(6*(1+13+2)) = 437.5kbps
    CAN1->BTR = (1 << CAN_BTR_SJW_Pos) |   // SJW = 2
                (13 << CAN_BTR_TS1_Pos) |  // TS1 = 14
                (1 << CAN_BTR_TS2_Pos) |   // TS2 = 2
                (5 << CAN_BTR_BRP_Pos);    // BRP = 6

    // Configure filters (accept all)
    CAN1->FMR |= CAN_FMR_FINIT;
    CAN1->FA1R &= ~CAN_FA1R_FACT0;
    CAN1->FM1R &= ~CAN_FM1R_FBM0;   // Mask mode
    CAN1->FS1R |= CAN_FS1R_FSC0;    // 32-bit scale
    CAN1->sFilterRegister[0].FR1 = 0;
    CAN1->sFilterRegister[0].FR2 = 0;
    CAN1->FA1R |= CAN_FA1R_FACT0;
    CAN1->FMR &= ~CAN_FMR_FINIT;

    // Leave initialization mode
    CAN1->MCR &= ~CAN_MCR_INRQ;
    while (CAN1->MSR & CAN_MSR_INAK);

    // Enable FIFO interrupts
    CAN1->IER |= CAN_IER_FMPIE0;
    NVIC_EnableIRQ(CAN1_RX0_IRQn);
}

bool CAN_Transmit(uint32_t id, uint8_t *data, uint8_t len) {
    // Find empty mailbox
    if (!(CAN1->TSR & CAN_TSR_TME0)) return false;

    // Set identifier
    CAN1->sTxMailBox[0].TIR = (id << CAN_TI0R_STID_Pos);

    // Set data length
    CAN1->sTxMailBox[0].TDTR = len;

    // Set data
    CAN1->sTxMailBox[0].TDLR = ((uint32_t)data[3] << 24) |
                               ((uint32_t)data[2] << 16) |
                               ((uint32_t)data[1] << 8) |
                               ((uint32_t)data[0]);
    CAN1->sTxMailBox[0].TDHR = ((uint32_t)data[7] << 24) |
                               ((uint32_t)data[6] << 16) |
                               ((uint32_t)data[5] << 8) |
                               ((uint32_t)data[4]);

    // Request transmission
    CAN1->sTxMailBox[0].TIR |= CAN_TI0R_TXRQ;

    return true;
}

typedef struct {
    uint32_t id;
    uint8_t data[8];
    uint8_t len;
} CANMessage_t;

bool CAN_Receive(CANMessage_t *msg) {
    if (!(CAN1->RF0R & CAN_RF0R_FMP0)) {
        return false;  // No message
    }

    // Read identifier
    msg->id = (CAN1->sFIFOMailBox[0].RIR >> CAN_RI0R_STID_Pos) & 0x7FF;

    // Read data length
    msg->len = CAN1->sFIFOMailBox[0].RDTR & CAN_RDT0R_DLC;

    // Read data
    uint32_t low = CAN1->sFIFOMailBox[0].RDLR;
    uint32_t high = CAN1->sFIFOMailBox[0].RDHR;

    msg->data[0] = (low >> 0) & 0xFF;
    msg->data[1] = (low >> 8) & 0xFF;
    msg->data[2] = (low >> 16) & 0xFF;
    msg->data[3] = (low >> 24) & 0xFF;
    msg->data[4] = (high >> 0) & 0xFF;
    msg->data[5] = (high >> 8) & 0xFF;
    msg->data[6] = (high >> 16) & 0xFF;
    msg->data[7] = (high >> 24) & 0xFF;

    // Release FIFO
    CAN1->RF0R |= CAN_RF0R_RFOM0;

    return true;
}
```

## Best Practices

- Always use timeouts to prevent infinite loops
- Implement error handling and recovery
- Use DMA for high-speed transfers
- Use interrupts to avoid polling
- Protect shared buffers with critical sections
- Validate received data (CRC, checksums)
- Implement protocol state machines properly
- Configure GPIO alternate functions correctly
- Calculate baud rates/timings accurately

---

## Reference: Memory Optimization

# Memory Optimization

## Code Size Optimization

```c
// Compiler flags for size optimization:
// -Os               : Optimize for size
// -ffunction-sections -fdata-sections : Separate functions/data
// -Wl,--gc-sections : Remove unused sections

// Use const for read-only data (stored in flash, not RAM)
const uint8_t lookup_table[256] = {
    0x00, 0x01, 0x02, /* ... */
};

// Use static to limit scope and enable optimization
static void InternalFunction(void) {
    // Only used in this file
}

// Inline small functions
static inline uint16_t Min(uint16_t a, uint16_t b) {
    return (a < b) ? a : b;
}

// Use appropriate data types
uint8_t small_value;      // Not int
bool is_ready;            // Not int
uint16_t medium_value;    // Not uint32_t if 16 bits enough

// Bit-fields for packed structures
typedef struct {
    uint8_t status : 3;      // 0-7
    uint8_t mode : 2;        // 0-3
    uint8_t error : 1;       // 0-1
    uint8_t ready : 1;       // 0-1
    uint8_t reserved : 1;
} __attribute__((packed)) StatusReg_t;

// Avoid unnecessary includes
// Only include what you need
```

## RAM Optimization

```c
// Share buffers when possible
#define BUFFER_SIZE 256
static uint8_t shared_buffer[BUFFER_SIZE];

void ProcessA(void) {
    // Use shared_buffer
    memset(shared_buffer, 0, BUFFER_SIZE);
    // Process...
}

void ProcessB(void) {
    // Reuse same buffer (not called simultaneously with ProcessA)
    memset(shared_buffer, 0, BUFFER_SIZE);
    // Process...
}

// Use unions for overlapping data
typedef union {
    uint8_t bytes[4];
    uint32_t word;
    float value;
} DataUnion_t;

// Stack vs heap allocation
void BadExample(void) {
    uint8_t *buffer = malloc(1024);  // Heap allocation, fragmentation risk
    // Use buffer...
    free(buffer);
}

void GoodExample(void) {
    uint8_t buffer[1024];  // Stack allocation (if stack permits)
    // Use buffer...
}  // Automatically freed

// Static allocation for predictable behavior
#define MAX_MESSAGES 10
typedef struct {
    CANMessage_t messages[MAX_MESSAGES];
    uint8_t count;
} MessageQueue_t;

static MessageQueue_t message_queue;  // Fixed size, no malloc

// Memory pools for dynamic allocation
#define POOL_SIZE 10
typedef struct {
    uint8_t buffer[64];
    bool in_use;
} MemBlock_t;

static MemBlock_t mem_pool[POOL_SIZE];

MemBlock_t* AllocBlock(void) {
    for (int i = 0; i < POOL_SIZE; i++) {
        if (!mem_pool[i].in_use) {
            mem_pool[i].in_use = true;
            return &mem_pool[i];
        }
    }
    return NULL;  // Pool exhausted
}

void FreeBlock(MemBlock_t *block) {
    if (block >= mem_pool && block < mem_pool + POOL_SIZE) {
        block->in_use = false;
    }
}
```

## Flash Memory Management

```c
// Store constants in flash with PROGMEM (AVR example)
// Or use const in ARM (automatically placed in flash)

// Large lookup tables
const uint16_t sine_table[360] = {
    0, 17, 34, 52, 69, 87, /* ... */
};

// String constants in flash
const char error_msg[] = "Error: Invalid parameter";

// Access flash data directly (ARM)
void UseFlashData(void) {
    uint16_t value = sine_table[90];  // Read from flash
    printf("%s\n", error_msg);        // String from flash
}

// Flash wear leveling for EEPROM emulation
#define FLASH_PAGE_SIZE 2048
#define FLASH_START_ADDR 0x0807F000

typedef struct {
    uint16_t id;
    uint16_t data;
    uint32_t checksum;
} FlashRecord_t;

bool Flash_WriteRecord(uint16_t id, uint16_t data) {
    // Find next available slot
    uint32_t addr = FLASH_START_ADDR;

    while (addr < FLASH_START_ADDR + FLASH_PAGE_SIZE) {
        FlashRecord_t *record = (FlashRecord_t*)addr;

        if (record->id == 0xFFFF) {
            // Empty slot found
            FlashRecord_t new_record = {
                .id = id,
                .data = data,
                .checksum = id + data
            };

            HAL_FLASH_Unlock();
            HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, addr, *(uint32_t*)&new_record);
            HAL_FLASH_Lock();

            return true;
        }

        addr += sizeof(FlashRecord_t);
    }

    // Page full - erase and write
    HAL_FLASH_Unlock();
    FLASH_EraseInitTypeDef erase = {
        .TypeErase = FLASH_TYPEERASE_PAGES,
        .PageAddress = FLASH_START_ADDR,
        .NbPages = 1
    };
    uint32_t error;
    HAL_FLASHEx_Erase(&erase, &error);
    HAL_FLASH_Lock();

    return Flash_WriteRecord(id, data);
}
```

## Stack Optimization

```c
// Monitor stack usage (FreeRTOS)
void CheckStackUsage(void) {
    UBaseType_t high_water = uxTaskGetStackHighWaterMark(NULL);
    printf("Stack remaining: %u words\n", high_water);
}

// Reduce local variable size
void BadFunction(void) {
    uint8_t large_buffer[2048];  // Large stack usage
    // ...
}

void GoodFunction(void) {
    static uint8_t large_buffer[2048];  // In BSS, not stack
    // ...
}

// Limit recursion depth
#define MAX_RECURSION_DEPTH 5

int RecursiveFunction(int n, int depth) {
    if (depth > MAX_RECURSION_DEPTH) {
        return -1;  // Prevent stack overflow
    }

    if (n <= 1) return n;
    return RecursiveFunction(n - 1, depth + 1) + RecursiveFunction(n - 2, depth + 1);
}

// Use iteration instead of recursion
int IterativeFunction(int n) {
    if (n <= 1) return n;

    int prev2 = 0, prev1 = 1;
    for (int i = 2; i <= n; i++) {
        int current = prev1 + prev2;
        prev2 = prev1;
        prev1 = current;
    }

    return prev1;
}
```

## Data Structure Optimization

```c
// Packed structures to save RAM
typedef struct {
    uint32_t timestamp;
    uint16_t value;
    uint8_t status;
    uint8_t checksum;
} __attribute__((packed)) DataRecord_t;  // 8 bytes instead of 12

// Ring buffer for efficient FIFO
typedef struct {
    uint8_t buffer[256];
    uint8_t head;
    uint8_t tail;  // Wraps at 256, no modulo needed
} RingBuffer_t;

void RingBuffer_Put(RingBuffer_t *rb, uint8_t data) {
    rb->buffer[rb->head++] = data;  // Auto-wraps due to uint8_t
}

uint8_t RingBuffer_Get(RingBuffer_t *rb) {
    return rb->buffer[rb->tail++];  // Auto-wraps
}

// Bit manipulation for flags
typedef struct {
    uint32_t flags;  // 32 boolean flags in 4 bytes
} SystemFlags_t;

#define FLAG_READY      (1 << 0)
#define FLAG_ERROR      (1 << 1)
#define FLAG_CALIBRATED (1 << 2)

void SetFlag(SystemFlags_t *sf, uint32_t flag) {
    sf->flags |= flag;
}

void ClearFlag(SystemFlags_t *sf, uint32_t flag) {
    sf->flags &= ~flag;
}

bool CheckFlag(SystemFlags_t *sf, uint32_t flag) {
    return (sf->flags & flag) != 0;
}

// Compact state machines
typedef enum {
    STATE_IDLE = 0,
    STATE_INIT,
    STATE_ACTIVE,
    STATE_ERROR
} State_t;

typedef struct {
    State_t state : 3;  // Only 3 bits needed for 4 states
    uint8_t retry_count : 5;
} StateMachine_t;
```

## Memory Monitoring

```c
// Linker script symbols
extern uint32_t _estack;
extern uint32_t _sdata;
extern uint32_t _edata;
extern uint32_t _sbss;
extern uint32_t _ebss;
extern uint32_t _heap_start;
extern uint32_t _heap_end;

// Calculate memory usage
void PrintMemoryUsage(void) {
    uint32_t data_size = (uint32_t)&_edata - (uint32_t)&_sdata;
    uint32_t bss_size = (uint32_t)&_ebss - (uint32_t)&_sbss;
    uint32_t heap_size = (uint32_t)&_heap_end - (uint32_t)&_heap_start;

    printf("Data: %u bytes\n", data_size);
    printf("BSS: %u bytes\n", bss_size);
    printf("Heap: %u bytes\n", heap_size);
    printf("Total RAM: %u bytes\n", data_size + bss_size + heap_size);
}

// Stack painting for usage analysis
void PaintStack(void) {
    extern uint32_t _estack;
    uint32_t stack_top = (uint32_t)&_estack;
    uint32_t current_sp;

    __asm volatile("MOV %0, SP" : "=r"(current_sp));

    for (uint32_t addr = current_sp; addr < stack_top; addr += 4) {
        *(uint32_t*)addr = 0xDEADBEEF;
    }
}

uint32_t GetStackUsage(void) {
    extern uint32_t _estack;
    uint32_t stack_top = (uint32_t)&_estack;
    uint32_t addr = stack_top - 1024;  // Assume 1KB stack

    while (addr < stack_top) {
        if (*(uint32_t*)addr != 0xDEADBEEF) {
            break;
        }
        addr += 4;
    }

    return stack_top - addr;
}
```

## Compile-Time Memory Analysis

```c
// Use static_assert to enforce limits
_Static_assert(sizeof(DataRecord_t) <= 16, "DataRecord too large");
_Static_assert(sizeof(StatusReg_t) == 1, "StatusReg not packed");

// Compile-time size calculations
#define ARRAY_SIZE(x) (sizeof(x) / sizeof((x)[0]))

const uint8_t config_data[] = {1, 2, 3, 4, 5};
#define CONFIG_SIZE ARRAY_SIZE(config_data)  // Known at compile time

// Check array bounds at compile time
void SetConfig(uint8_t index, uint8_t value) {
    _Static_assert(CONFIG_SIZE < 256, "Config index must fit in uint8_t");

    if (index < CONFIG_SIZE) {
        // Safe access
    }
}
```

## Optimization Techniques Summary

```c
// 1. Use smallest appropriate data types
uint8_t  counter;        // Not int
bool     flag;           // Not int

// 2. Pack structures
typedef struct {
    uint16_t id;
    uint8_t status;
    uint8_t checksum;
} __attribute__((packed)) Header_t;

// 3. Use const for read-only data (goes to flash)
const uint8_t lookup[256] = { /* ... */ };

// 4. Share buffers
static uint8_t work_buffer[512];

// 5. Use memory pools instead of malloc
static Block_t pool[10];

// 6. Limit stack usage
static uint8_t large_array[1024];  // Not on stack

// 7. Use bit-fields for flags
typedef struct {
    uint8_t ready : 1;
    uint8_t error : 1;
    uint8_t mode : 3;
} Flags_t;

// 8. Enable compiler optimizations
// -Os -ffunction-sections -fdata-sections -Wl,--gc-sections

// 9. Monitor usage
printf("Free heap: %u\n", xPortGetFreeHeapSize());
printf("Stack high water: %u\n", uxTaskGetStackHighWaterMark(NULL));

// 10. Profile and measure
// Use .map file to identify large symbols
// Use size tool: arm-none-eabi-size firmware.elf
```

## Linker Script Customization

```ld
/* Custom linker script sections */
MEMORY
{
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
    RAM (rwx)   : ORIGIN = 0x20000000, LENGTH = 128K
}

SECTIONS
{
    .text : {
        *(.isr_vector)
        *(.text*)
        *(.rodata*)
    } > FLASH

    .data : {
        _sdata = .;
        *(.data*)
        _edata = .;
    } > RAM AT > FLASH

    .bss : {
        _sbss = .;
        *(.bss*)
        *(COMMON)
        _ebss = .;
    } > RAM

    /* Reserve space for heap */
    .heap : {
        _heap_start = .;
        . = . + 10K;
        _heap_end = .;
    } > RAM
}
```

## Best Practices

- Use const for all read-only data
- Prefer static allocation over dynamic
- Pack structures with `__attribute__((packed))`
- Use smallest data types possible
- Share buffers when tasks don't overlap
- Monitor heap and stack usage regularly
- Enable link-time optimization (-flto)
- Remove unused code with -ffunction-sections
- Profile with .map file and size tool
- Test with minimal memory configuration

---

## Reference: Microcontroller Programming

# Microcontroller Programming

## GPIO Configuration (STM32)

```c
#include "stm32f4xx.h"

// Configure GPIO pin as output
void GPIO_Init_Output(GPIO_TypeDef *port, uint32_t pin) {
    // Enable clock for GPIO port
    if (port == GPIOA) RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    else if (port == GPIOB) RCC->AHB1ENR |= RCC_AHB1ENR_GPIOBEN;
    else if (port == GPIOC) RCC->AHB1ENR |= RCC_AHB1ENR_GPIOCEN;

    // Set mode to output (01)
    port->MODER &= ~(0x3 << (pin * 2));
    port->MODER |= (0x1 << (pin * 2));

    // Set output type to push-pull
    port->OTYPER &= ~(1 << pin);

    // Set speed to high
    port->OSPEEDR |= (0x3 << (pin * 2));

    // No pull-up/pull-down
    port->PUPDR &= ~(0x3 << (pin * 2));
}

// Configure GPIO pin as input with pull-up
void GPIO_Init_Input_PullUp(GPIO_TypeDef *port, uint32_t pin) {
    // Enable clock
    if (port == GPIOA) RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;

    // Set mode to input (00)
    port->MODER &= ~(0x3 << (pin * 2));

    // Set pull-up (01)
    port->PUPDR &= ~(0x3 << (pin * 2));
    port->PUPDR |= (0x1 << (pin * 2));
}

// Toggle GPIO pin
static inline void GPIO_Toggle(GPIO_TypeDef *port, uint32_t pin) {
    port->ODR ^= (1 << pin);
}

// Read GPIO pin
static inline bool GPIO_Read(GPIO_TypeDef *port, uint32_t pin) {
    return (port->IDR & (1 << pin)) != 0;
}

// Write GPIO pin (using BSRR for atomic operation)
static inline void GPIO_Write(GPIO_TypeDef *port, uint32_t pin, bool state) {
    if (state) {
        port->BSRR = (1 << pin);  // Set
    } else {
        port->BSRR = (1 << (pin + 16));  // Reset
    }
}
```

## Timer Configuration

```c
// Configure TIM2 for 1kHz interrupt (84MHz clock)
void Timer_Init_1kHz(void) {
    // Enable TIM2 clock
    RCC->APB1ENR |= RCC_APB1ENR_TIM2EN;

    // Configure prescaler and auto-reload
    // 84MHz / 84 = 1MHz, 1MHz / 1000 = 1kHz
    TIM2->PSC = 84 - 1;     // Prescaler
    TIM2->ARR = 1000 - 1;   // Auto-reload

    // Enable update interrupt
    TIM2->DIER |= TIM_DIER_UIE;

    // Enable TIM2 interrupt in NVIC
    NVIC_SetPriority(TIM2_IRQn, 2);
    NVIC_EnableIRQ(TIM2_IRQn);

    // Start timer
    TIM2->CR1 |= TIM_CR1_CEN;
}

// Timer interrupt handler
void TIM2_IRQHandler(void) {
    if (TIM2->SR & TIM_SR_UIF) {
        TIM2->SR &= ~TIM_SR_UIF;  // Clear flag

        // 1kHz tick
        SystemTick();
    }
}

// PWM configuration (50% duty cycle, 1kHz)
void PWM_Init(void) {
    RCC->APB1ENR |= RCC_APB1ENR_TIM3EN;

    // Configure timer for PWM
    TIM3->PSC = 84 - 1;     // 1MHz
    TIM3->ARR = 1000 - 1;   // 1kHz

    // PWM mode 1 on channel 1
    TIM3->CCMR1 |= (0x6 << TIM_CCMR1_OC1M_Pos);
    TIM3->CCMR1 |= TIM_CCMR1_OC1PE;

    // 50% duty cycle
    TIM3->CCR1 = 500;

    // Enable output
    TIM3->CCER |= TIM_CCER_CC1E;

    // Start timer
    TIM3->CR1 |= TIM_CR1_CEN;
}

// Set PWM duty cycle (0-1000)
void PWM_SetDutyCycle(uint16_t duty) {
    TIM3->CCR1 = duty;
}
```

## External Interrupt (EXTI)

```c
// Configure PA0 as external interrupt (rising edge)
void EXTI_Init_PA0(void) {
    // Enable GPIOA and SYSCFG clocks
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    RCC->APB2ENR |= RCC_APB2ENR_SYSCFGEN;

    // Configure PA0 as input
    GPIOA->MODER &= ~GPIO_MODER_MODER0;

    // Connect EXTI0 to PA0
    SYSCFG->EXTICR[0] &= ~SYSCFG_EXTICR1_EXTI0;
    SYSCFG->EXTICR[0] |= SYSCFG_EXTICR1_EXTI0_PA;

    // Configure EXTI0
    EXTI->IMR |= EXTI_IMR_MR0;      // Unmask interrupt
    EXTI->RTSR |= EXTI_RTSR_TR0;    // Rising edge trigger

    // Enable EXTI0 interrupt in NVIC
    NVIC_SetPriority(EXTI0_IRQn, 3);
    NVIC_EnableIRQ(EXTI0_IRQn);
}

// EXTI0 interrupt handler
void EXTI0_IRQHandler(void) {
    if (EXTI->PR & EXTI_PR_PR0) {
        EXTI->PR = EXTI_PR_PR0;  // Clear pending flag

        // Handle button press
        Button_Pressed();
    }
}
```

## ADC Configuration

```c
// Configure ADC1 for single conversion
void ADC_Init(void) {
    // Enable ADC1 clock
    RCC->APB2ENR |= RCC_APB2ENR_ADC1EN;

    // Configure ADC
    ADC1->CR2 = 0;
    ADC1->CR1 = 0;

    // 12-bit resolution
    ADC1->CR1 &= ~ADC_CR1_RES;

    // Single conversion mode
    ADC1->CR2 &= ~ADC_CR2_CONT;

    // Right alignment
    ADC1->CR2 &= ~ADC_CR2_ALIGN;

    // Regular sequence length = 1
    ADC1->SQR1 = 0;

    // Power on ADC
    ADC1->CR2 |= ADC_CR2_ADON;
}

// Read ADC channel
uint16_t ADC_Read(uint8_t channel) {
    // Set channel in regular sequence
    ADC1->SQR3 = channel;

    // Start conversion
    ADC1->CR2 |= ADC_CR2_SWSTART;

    // Wait for conversion complete
    while (!(ADC1->SR & ADC_SR_EOC));

    // Return result
    return ADC1->DR;
}

// ADC with DMA (continuous conversion)
void ADC_Init_DMA(void) {
    // Enable DMA2 clock
    RCC->AHB1ENR |= RCC_AHB1ENR_DMA2EN;

    // Configure DMA2 Stream 0 Channel 0 for ADC1
    DMA2_Stream0->CR = 0;
    while (DMA2_Stream0->CR & DMA_SxCR_EN);  // Wait for disable

    DMA2_Stream0->PAR = (uint32_t)&(ADC1->DR);
    DMA2_Stream0->M0AR = (uint32_t)adc_buffer;
    DMA2_Stream0->NDTR = ADC_BUFFER_SIZE;

    DMA2_Stream0->CR = (0 << DMA_SxCR_CHSEL_Pos) |  // Channel 0
                       (1 << DMA_SxCR_MSIZE_Pos) |  // 16-bit memory
                       (1 << DMA_SxCR_PSIZE_Pos) |  // 16-bit peripheral
                       DMA_SxCR_MINC |               // Memory increment
                       DMA_SxCR_CIRC |               // Circular mode
                       DMA_SxCR_EN;                  // Enable

    // Enable ADC DMA mode
    ADC1->CR2 |= ADC_CR2_DMA | ADC_CR2_DDS;

    // Enable continuous conversion
    ADC1->CR2 |= ADC_CR2_CONT;

    // Start conversion
    ADC1->CR2 |= ADC_CR2_SWSTART;
}
```

## UART Communication

```c
// Configure USART2 (115200 baud, 8N1)
void UART_Init(void) {
    // Enable USART2 and GPIOA clocks
    RCC->APB1ENR |= RCC_APB1ENR_USART2EN;
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;

    // Configure PA2 (TX) and PA3 (RX) as alternate function
    GPIOA->MODER |= (2 << GPIO_MODER_MODER2_Pos) | (2 << GPIO_MODER_MODER3_Pos);
    GPIOA->AFR[0] |= (7 << GPIO_AFRL_AFRL2_Pos) | (7 << GPIO_AFRL_AFRL3_Pos);

    // Configure USART2
    // 84MHz / 115200 = 729 = 0x2D9
    USART2->BRR = 0x2D9;

    // Enable TX, RX, and USART
    USART2->CR1 = USART_CR1_TE | USART_CR1_RE | USART_CR1_UE;
}

// Send byte
void UART_SendByte(uint8_t data) {
    while (!(USART2->SR & USART_SR_TXE));
    USART2->DR = data;
}

// Receive byte
uint8_t UART_ReceiveByte(void) {
    while (!(USART2->SR & USART_SR_RXNE));
    return USART2->DR;
}

// Send string
void UART_SendString(const char *str) {
    while (*str) {
        UART_SendByte(*str++);
    }
}
```

## System Clock Configuration

```c
// Configure system clock to 168MHz (STM32F4)
void SystemClock_Config(void) {
    // Enable HSE
    RCC->CR |= RCC_CR_HSEON;
    while (!(RCC->CR & RCC_CR_HSERDY));

    // Configure flash latency (5 wait states for 168MHz)
    FLASH->ACR = FLASH_ACR_PRFTEN | FLASH_ACR_ICEN | FLASH_ACR_DCEN | FLASH_ACR_LATENCY_5WS;

    // Configure PLL: HSE=8MHz, VCO=336MHz, SYSCLK=168MHz
    // PLL_VCO = (HSE / PLLM) * PLLN = (8 / 8) * 336 = 336MHz
    // SYSCLK = PLL_VCO / PLLP = 336 / 2 = 168MHz
    RCC->PLLCFGR = (8 << RCC_PLLCFGR_PLLM_Pos) |
                   (336 << RCC_PLLCFGR_PLLN_Pos) |
                   (0 << RCC_PLLCFGR_PLLP_Pos) |  // PLLP = 2
                   RCC_PLLCFGR_PLLSRC_HSE |
                   (7 << RCC_PLLCFGR_PLLQ_Pos);

    // Enable PLL
    RCC->CR |= RCC_CR_PLLON;
    while (!(RCC->CR & RCC_CR_PLLRDY));

    // Configure AHB, APB1, APB2 prescalers
    RCC->CFGR = RCC_CFGR_HPRE_DIV1 |   // AHB = 168MHz
                RCC_CFGR_PPRE1_DIV4 |  // APB1 = 42MHz
                RCC_CFGR_PPRE2_DIV2;   // APB2 = 84MHz

    // Switch to PLL
    RCC->CFGR |= RCC_CFGR_SW_PLL;
    while ((RCC->CFGR & RCC_CFGR_SWS) != RCC_CFGR_SWS_PLL);

    // Update SystemCoreClock variable
    SystemCoreClock = 168000000;
}
```

## Watchdog Timer

```c
// Configure independent watchdog (IWDG)
void Watchdog_Init(void) {
    // Enable write access to IWDG registers
    IWDG->KR = 0x5555;

    // Set prescaler to 64 (40kHz / 64 = 625Hz)
    IWDG->PR = IWDG_PR_PR_2;

    // Set reload value (625Hz / 625 = 1s timeout)
    IWDG->RLR = 625;

    // Reload counter
    IWDG->KR = 0xAAAA;

    // Start watchdog
    IWDG->KR = 0xCCCC;
}

// Reset watchdog
void Watchdog_Refresh(void) {
    IWDG->KR = 0xAAAA;
}
```

## Low-Power Modes

```c
// Enter sleep mode (CPU stopped, peripherals running)
void Enter_Sleep(void) {
    __WFI();  // Wait for interrupt
}

// Enter stop mode (all clocks stopped except LSI/LSE)
void Enter_Stop(void) {
    // Clear wakeup flags
    PWR->CR |= PWR_CR_CWUF;

    // Set SLEEPDEEP bit
    SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;

    // Enter stop mode
    PWR->CR &= ~PWR_CR_PDDS;
    PWR->CR |= PWR_CR_LPDS;

    __WFI();

    // Reconfigure clocks after wakeup
    SystemClock_Config();
}

// Enter standby mode (lowest power, RAM lost)
void Enter_Standby(void) {
    // Enable wakeup pin
    PWR->CSR |= PWR_CSR_EWUP;

    // Clear wakeup flags
    PWR->CR |= PWR_CR_CWUF;

    // Set SLEEPDEEP bit
    SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;

    // Enter standby mode
    PWR->CR |= PWR_CR_PDDS;

    __WFI();
}
```

## Best Practices

- Always use `volatile` for hardware register access
- Use bit-banding for atomic single-bit operations
- Clear interrupt flags in ISRs to prevent re-entry
- Configure clock tree before enabling peripherals
- Use BSRR register for atomic GPIO writes
- Enable interrupts with appropriate priorities
- Add timeout checks for polling operations
- Protect RMW operations with critical sections if needed

---

## Reference: Power Optimization

# Power Optimization

## Sleep Mode Strategy

```c
#include "stm32f4xx.h"

typedef enum {
    POWER_MODE_RUN,
    POWER_MODE_SLEEP,
    POWER_MODE_STOP,
    POWER_MODE_STANDBY
} PowerMode_t;

// Power mode with peripheral activity tracking
typedef struct {
    uint32_t run_time_ms;
    uint32_t sleep_time_ms;
    uint32_t stop_time_ms;
    uint32_t active_peripherals;
} PowerProfile_t;

// Enter appropriate sleep mode based on wakeup time
void EnterLowPower(uint32_t sleep_duration_ms) {
    if (sleep_duration_ms < 10) {
        // Very short sleep - just WFI
        __WFI();
    } else if (sleep_duration_ms < 1000) {
        // Short sleep - sleep mode (fast wakeup)
        EnterSleepMode();
    } else {
        // Long sleep - stop mode (lower power)
        EnterStopMode(sleep_duration_ms);
    }
}

void EnterSleepMode(void) {
    // Disable SysTick interrupt to prevent wakeup
    SysTick->CTRL &= ~SysTick_CTRL_TICKINT_Msk;

    // Enter sleep mode
    __WFI();

    // Re-enable SysTick
    SysTick->CTRL |= SysTick_CTRL_TICKINT_Msk;
}

void EnterStopMode(uint32_t sleep_ms) {
    // Configure RTC wakeup if needed
    if (sleep_ms > 0) {
        RTC_SetWakeup(sleep_ms);
    }

    // Disable peripherals before stop
    DisableUnusedPeripherals();

    // Enter stop mode with regulator in low-power mode
    PWR->CR |= PWR_CR_LPDS;
    PWR->CR &= ~PWR_CR_PDDS;
    SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;

    __WFI();

    // Restore system clock after wakeup
    SystemClock_Config();

    // Re-enable peripherals
    RestorePeripherals();
}
```

## Dynamic Clock Scaling

```c
typedef enum {
    CLOCK_SPEED_LOW = 0,     // 48MHz
    CLOCK_SPEED_MEDIUM,      // 84MHz
    CLOCK_SPEED_HIGH         // 168MHz
} ClockSpeed_t;

void SetSystemClock(ClockSpeed_t speed) {
    switch (speed) {
        case CLOCK_SPEED_LOW:
            // 48MHz - lowest power for low-performance tasks
            ConfigurePLL(8, 96, 2, 2);  // VCO=96MHz, SYSCLK=48MHz
            SystemCoreClock = 48000000;
            break;

        case CLOCK_SPEED_MEDIUM:
            // 84MHz - medium power
            ConfigurePLL(8, 168, 2, 2);
            SystemCoreClock = 84000000;
            break;

        case CLOCK_SPEED_HIGH:
            // 168MHz - full performance
            ConfigurePLL(8, 336, 2, 2);
            SystemCoreClock = 168000000;
            break;
    }

    // Update peripheral clocks
    UpdatePeripheralClocks();
}

// Automatic clock scaling based on workload
void AdaptiveClock(void) {
    static uint32_t idle_ticks = 0;
    static uint32_t total_ticks = 0;

    total_ticks++;

    if (IsIdle()) {
        idle_ticks++;
    }

    // Check every second
    if (total_ticks >= 1000) {
        uint32_t load_percent = 100 - (idle_ticks * 100 / total_ticks);

        if (load_percent > 80) {
            SetSystemClock(CLOCK_SPEED_HIGH);
        } else if (load_percent > 40) {
            SetSystemClock(CLOCK_SPEED_MEDIUM);
        } else {
            SetSystemClock(CLOCK_SPEED_LOW);
        }

        idle_ticks = 0;
        total_ticks = 0;
    }
}
```

## Peripheral Power Management

```c
// Smart peripheral enabling/disabling
typedef struct {
    uint32_t last_used_ms;
    bool is_enabled;
    uint32_t timeout_ms;
} PeripheralPower_t;

PeripheralPower_t i2c_power = {0, false, 1000};
PeripheralPower_t uart_power = {0, false, 5000};

void EnablePeripheral_I2C(void) {
    if (!i2c_power.is_enabled) {
        RCC->APB1ENR |= RCC_APB1ENR_I2C1EN;
        i2c_power.is_enabled = true;
    }
    i2c_power.last_used_ms = HAL_GetTick();
}

void DisableUnusedPeripherals(void) {
    uint32_t current_time = HAL_GetTick();

    // Auto-disable I2C if not used recently
    if (i2c_power.is_enabled) {
        if ((current_time - i2c_power.last_used_ms) > i2c_power.timeout_ms) {
            RCC->APB1ENR &= ~RCC_APB1ENR_I2C1EN;
            i2c_power.is_enabled = false;
        }
    }

    // Auto-disable UART
    if (uart_power.is_enabled) {
        if ((current_time - uart_power.last_used_ms) > uart_power.timeout_ms) {
            RCC->APB1ENR &= ~RCC_APB1ENR_USART2EN;
            uart_power.is_enabled = false;
        }
    }
}

// Disable all non-essential peripherals
void MinimizePower(void) {
    // Disable unused GPIO clocks
    RCC->AHB1ENR &= ~(RCC_AHB1ENR_GPIODEN | RCC_AHB1ENR_GPIOEEN);

    // Disable unused timers
    RCC->APB1ENR &= ~(RCC_APB1ENR_TIM3EN | RCC_APB1ENR_TIM4EN);

    // Disable USB if not used
    RCC->AHB2ENR &= ~RCC_AHB2ENR_OTGFSEN;

    // Disable DMA if not needed
    RCC->AHB1ENR &= ~(RCC_AHB1ENR_DMA1EN | RCC_AHB1ENR_DMA2EN);
}
```

## GPIO Power Optimization

```c
// Configure unused pins to minimize leakage
void ConfigureUnusedPins(void) {
    // All unused pins: analog mode (lowest power)
    GPIOD->MODER = 0xFFFFFFFF;  // All pins analog
    GPIOE->MODER = 0xFFFFFFFF;
    GPIOF->MODER = 0xFFFFFFFF;

    // Alternatively: output low
    // GPIOD->MODER = 0x55555555;  // All output
    // GPIOD->ODR = 0x0000;        // All low
}

// Configure GPIO for minimum power in sleep
void PrepareGPIOForSleep(void) {
    // Save current GPIO state
    uint32_t gpioa_moder = GPIOA->MODER;

    // Set all to analog mode (except wakeup pins)
    GPIOA->MODER = 0xFFFFFFFF;
    GPIOB->MODER = 0xFFFFFFFF;
    GPIOC->MODER = 0xFFFFFFFF;

    // Keep PA0 as input for wakeup
    GPIOA->MODER &= ~(0x3 << 0);

    // Enter sleep...
    EnterStopMode(0);

    // Restore GPIO configuration
    GPIOA->MODER = gpioa_moder;
}
```

## ADC Power Optimization

```c
// ADC with automatic power-down
void ADC_LowPower_Init(void) {
    RCC->APB2ENR |= RCC_APB2ENR_ADC1EN;

    // Enable auto power-down mode
    ADC1->CR1 &= ~ADC_CR1_RES;  // 12-bit resolution

    // Discontinuous mode
    ADC1->CR1 |= ADC_CR1_DISCEN;

    // Power on only when needed
    ADC1->CR2 &= ~ADC_CR2_ADON;
}

uint16_t ADC_ReadLowPower(uint8_t channel) {
    // Power on ADC
    ADC1->CR2 |= ADC_CR2_ADON;

    // Wait for ADC ready (few microseconds)
    for (volatile int i = 0; i < 100; i++);

    // Configure channel
    ADC1->SQR3 = channel;

    // Start conversion
    ADC1->CR2 |= ADC_CR2_SWSTART;

    // Wait for completion
    while (!(ADC1->SR & ADC_SR_EOC));

    uint16_t result = ADC1->DR;

    // Power down ADC
    ADC1->CR2 &= ~ADC_CR2_ADON;

    return result;
}
```

## Battery Monitoring

```c
// Battery voltage monitoring with low-power ADC
#define VREFINT_CAL_ADDR  ((uint16_t*)0x1FFF7A2A)
#define VREFINT_CAL_VREF  3300  // mV

uint16_t GetBatteryVoltage_mV(void) {
    // Read internal reference voltage
    uint16_t vrefint_data = ADC_ReadLowPower(17);  // Internal VREF channel

    // Calculate actual VDDA
    uint32_t vdda = 3300 * (*VREFINT_CAL_ADDR) / vrefint_data;

    // Read battery voltage divider (e.g., on ADC channel 0)
    uint16_t battery_raw = ADC_ReadLowPower(0);

    // Assuming 2:1 voltage divider
    uint32_t battery_mv = (vdda * battery_raw / 4096) * 2;

    return battery_mv;
}

// Battery state estimation
typedef enum {
    BATTERY_FULL,
    BATTERY_GOOD,
    BATTERY_LOW,
    BATTERY_CRITICAL
} BatteryState_t;

BatteryState_t GetBatteryState(void) {
    uint16_t voltage = GetBatteryVoltage_mV();

    if (voltage > 3700) return BATTERY_FULL;
    else if (voltage > 3400) return BATTERY_GOOD;
    else if (voltage > 3200) return BATTERY_LOW;
    else return BATTERY_CRITICAL;
}

// Adaptive behavior based on battery
void AdaptToBattery(void) {
    BatteryState_t state = GetBatteryState();

    switch (state) {
        case BATTERY_FULL:
        case BATTERY_GOOD:
            // Normal operation
            SetSystemClock(CLOCK_SPEED_HIGH);
            SetSamplingRate(100);  // 100Hz
            break;

        case BATTERY_LOW:
            // Reduce performance
            SetSystemClock(CLOCK_SPEED_MEDIUM);
            SetSamplingRate(10);  // 10Hz
            break;

        case BATTERY_CRITICAL:
            // Minimum power mode
            SetSystemClock(CLOCK_SPEED_LOW);
            SetSamplingRate(1);  // 1Hz
            DisableNonEssentialFeatures();
            break;
    }
}
```

## RTC Wakeup

```c
// Configure RTC for periodic wakeup
void RTC_Init_Wakeup(void) {
    // Enable PWR clock
    RCC->APB1ENR |= RCC_APB1ENR_PWREN;

    // Enable access to RTC domain
    PWR->CR |= PWR_CR_DBP;

    // Enable LSI
    RCC->CSR |= RCC_CSR_LSION;
    while (!(RCC->CSR & RCC_CSR_LSIRDY));

    // Select LSI as RTC clock
    RCC->BDCR |= RCC_BDCR_RTCSEL_1;
    RCC->BDCR |= RCC_BDCR_RTCEN;

    // Disable RTC write protection
    RTC->WPR = 0xCA;
    RTC->WPR = 0x53;

    // Configure wakeup timer
    RTC->CR &= ~RTC_CR_WUTE;
    while (!(RTC->ISR & RTC_ISR_WUTWF));

    // Set wakeup auto-reload (1Hz with 37kHz LSI)
    RTC->WUTR = 37000 - 1;

    // Enable wakeup timer and interrupt
    RTC->CR |= RTC_CR_WUTIE | RTC_CR_WUTE;

    // Enable RTC wakeup interrupt in EXTI
    EXTI->IMR |= EXTI_IMR_MR22;
    EXTI->RTSR |= EXTI_RTSR_TR22;

    // Enable NVIC
    NVIC_EnableIRQ(RTC_WKUP_IRQn);
}

void RTC_WKUP_IRQHandler(void) {
    if (RTC->ISR & RTC_ISR_WUTF) {
        RTC->ISR &= ~RTC_ISR_WUTF;  // Clear flag
        EXTI->PR = EXTI_PR_PR22;     // Clear EXTI flag

        // Periodic wakeup action
        PeriodicTask();
    }
}
```

## Power Measurement

```c
// Estimate power consumption
typedef struct {
    uint32_t cpu_active_ms;
    uint32_t cpu_sleep_ms;
    uint32_t peripherals;  // Bitmap of active peripherals
    ClockSpeed_t clock_speed;
} PowerStats_t;

float EstimatePower_mA(PowerStats_t *stats) {
    float power = 0.0f;

    // CPU power based on clock speed and activity
    switch (stats->clock_speed) {
        case CLOCK_SPEED_HIGH:
            power += 30.0f;  // 30mA at 168MHz
            break;
        case CLOCK_SPEED_MEDIUM:
            power += 20.0f;  // 20mA at 84MHz
            break;
        case CLOCK_SPEED_LOW:
            power += 12.0f;  // 12mA at 48MHz
            break;
    }

    // Sleep mode power
    float sleep_ratio = (float)stats->cpu_sleep_ms / (stats->cpu_active_ms + stats->cpu_sleep_ms);
    power = power * (1.0f - sleep_ratio) + 0.5f * sleep_ratio;  // 0.5mA in sleep

    // Peripheral power
    if (stats->peripherals & PERIPH_UART) power += 1.0f;
    if (stats->peripherals & PERIPH_I2C) power += 0.5f;
    if (stats->peripherals & PERIPH_SPI) power += 1.5f;
    if (stats->peripherals & PERIPH_ADC) power += 2.0f;

    return power;
}
```

## Best Practices

- Use stop mode for sleeps > 1 second
- Configure unused pins as analog or output-low
- Disable peripheral clocks when not in use
- Use RTC wakeup instead of systick in low-power modes
- Reduce clock speed during low-activity periods
- Use DMA to reduce CPU wakeups
- Batch operations to minimize wakeup frequency
- Monitor battery and adapt behavior
- Profile actual power consumption with current meter

---

## Reference: Rtos Patterns

# RTOS Patterns

## Task Creation and Management

```c
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"

// Task priorities (0 = lowest, configMAX_PRIORITIES-1 = highest)
#define PRIORITY_SENSOR     (tskIDLE_PRIORITY + 2)
#define PRIORITY_PROCESSING (tskIDLE_PRIORITY + 1)
#define PRIORITY_COMM       (tskIDLE_PRIORITY + 3)

// Stack sizes (in words, not bytes)
#define STACK_SIZE_SENSOR   (256)
#define STACK_SIZE_PROCESS  (512)

void vSensorTask(void *pvParameters) {
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xFrequency = pdMS_TO_TICKS(100);  // 100ms period

    for (;;) {
        // Read sensor data
        uint16_t sensor_value = ADC_Read();

        // Send to processing queue
        xQueueSend(xProcessQueue, &sensor_value, pdMS_TO_TICKS(10));

        // Wait for next cycle (precise timing)
        vTaskDelayUntil(&xLastWakeTime, xFrequency);
    }
}

void vProcessingTask(void *pvParameters) {
    uint16_t received_data;

    for (;;) {
        // Block until data available
        if (xQueueReceive(xProcessQueue, &received_data, portMAX_DELAY) == pdPASS) {
            // Process data
            uint16_t result = ProcessSensorData(received_data);

            // Signal completion
            xSemaphoreGive(xProcessDoneSemaphore);
        }
    }
}

// Task creation in main()
void CreateTasks(void) {
    xTaskCreate(vSensorTask, "Sensor", STACK_SIZE_SENSOR, NULL,
                PRIORITY_SENSOR, &xSensorTaskHandle);
    xTaskCreate(vProcessingTask, "Process", STACK_SIZE_PROCESS, NULL,
                PRIORITY_PROCESSING, &xProcessTaskHandle);
}
```

## Queue Communication

```c
// Queue creation and usage
QueueHandle_t xDataQueue;
QueueHandle_t xCommandQueue;

void InitQueues(void) {
    // Create queue for 10 uint32_t items
    xDataQueue = xQueueCreate(10, sizeof(uint32_t));

    // Create queue for command structures
    xCommandQueue = xQueueCreate(5, sizeof(Command_t));

    if (xDataQueue == NULL || xCommandQueue == NULL) {
        // Handle error - insufficient heap
        Error_Handler();
    }
}

// Producer task
void vProducerTask(void *pvParameters) {
    uint32_t data = 0;

    for (;;) {
        data++;

        // Non-blocking send (timeout = 0)
        if (xQueueSend(xDataQueue, &data, 0) != pdPASS) {
            // Queue full - handle overflow
            DiscardOldData();
        }

        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

// Consumer task
void vConsumerTask(void *pvParameters) {
    uint32_t received;

    for (;;) {
        // Block indefinitely until data available
        if (xQueueReceive(xDataQueue, &received, portMAX_DELAY) == pdPASS) {
            ProcessData(received);
        }
    }
}
```

## Mutex and Critical Sections

```c
SemaphoreHandle_t xI2CMutex;
SemaphoreHandle_t xUARTMutex;

void InitMutexes(void) {
    xI2CMutex = xSemaphoreCreateMutex();
    xUARTMutex = xSemaphoreCreateMutex();

    if (xI2CMutex == NULL || xUARTMutex == NULL) {
        Error_Handler();
    }
}

// Safe shared resource access
bool I2C_Write(uint8_t addr, uint8_t *data, size_t len) {
    // Take mutex with timeout
    if (xSemaphoreTake(xI2CMutex, pdMS_TO_TICKS(100)) == pdTRUE) {
        // Critical section - exclusive I2C access
        bool result = HAL_I2C_Write(addr, data, len);

        // Always release mutex
        xSemaphoreGive(xI2CMutex);

        return result;
    }

    return false;  // Timeout
}

// Very short critical section (disables interrupts)
void UpdateSharedCounter(void) {
    taskENTER_CRITICAL();
    g_shared_counter++;
    taskEXIT_CRITICAL();
}
```

## Binary Semaphores (Signaling)

```c
SemaphoreHandle_t xDataReadySemaphore;

// Interrupt signals task
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    // Signal from ISR
    xSemaphoreGiveFromISR(xDataReadySemaphore, &xHigherPriorityTaskWoken);

    // Yield if higher priority task woken
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}

// Task waits for interrupt
void vADCTask(void *pvParameters) {
    for (;;) {
        // Wait for ADC completion (from ISR)
        if (xSemaphoreTake(xDataReadySemaphore, portMAX_DELAY) == pdTRUE) {
            uint16_t adc_value = HAL_ADC_GetValue(&hadc1);
            ProcessADCValue(adc_value);
        }
    }
}
```

## Software Timers

```c
TimerHandle_t xWatchdogTimer;
TimerHandle_t xBlinkTimer;

void vWatchdogCallback(TimerHandle_t xTimer) {
    // Periodic watchdog check
    if (!SystemHealthCheck()) {
        SystemReset();
    }
}

void vBlinkCallback(TimerHandle_t xTimer) {
    HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
}

void InitTimers(void) {
    // One-shot timer
    xWatchdogTimer = xTimerCreate("Watchdog", pdMS_TO_TICKS(5000),
                                   pdTRUE, 0, vWatchdogCallback);

    // Auto-reload timer
    xBlinkTimer = xTimerCreate("Blink", pdMS_TO_TICKS(500),
                               pdTRUE, 0, vBlinkCallback);

    // Start timers
    xTimerStart(xWatchdogTimer, 0);
    xTimerStart(xBlinkTimer, 0);
}
```

## Event Groups

```c
EventGroupHandle_t xSystemEvents;

#define EVENT_SENSOR_READY   (1 << 0)
#define EVENT_COMM_READY     (1 << 1)
#define EVENT_CALIBRATED     (1 << 2)
#define EVENT_ALL_READY      (EVENT_SENSOR_READY | EVENT_COMM_READY | EVENT_CALIBRATED)

void vInitTask(void *pvParameters) {
    // Initialize subsystems
    InitSensor();
    xEventGroupSetBits(xSystemEvents, EVENT_SENSOR_READY);

    InitComm();
    xEventGroupSetBits(xSystemEvents, EVENT_COMM_READY);

    Calibrate();
    xEventGroupSetBits(xSystemEvents, EVENT_CALIBRATED);

    vTaskDelete(NULL);  // Delete init task
}

void vMainTask(void *pvParameters) {
    // Wait for all subsystems ready
    xEventGroupWaitBits(xSystemEvents, EVENT_ALL_READY, pdFALSE, pdTRUE, portMAX_DELAY);

    // System fully initialized
    for (;;) {
        RunMainLoop();
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}
```

## Memory Management

```c
// FreeRTOSConfig.h settings
#define configTOTAL_HEAP_SIZE           ((size_t)(20 * 1024))  // 20KB heap
#define configMINIMAL_STACK_SIZE        ((uint16_t)128)
#define configUSE_MALLOC_FAILED_HOOK    1

// Heap usage monitoring
void PrintHeapStats(void) {
    size_t free_heap = xPortGetFreeHeapSize();
    size_t min_ever_free = xPortGetMinimumEverFreeHeapSize();

    printf("Heap Free: %u bytes\n", free_heap);
    printf("Min Ever Free: %u bytes\n", min_ever_free);
}

// Stack overflow hook (enable in FreeRTOSConfig.h)
void vApplicationStackOverflowHook(TaskHandle_t xTask, char *pcTaskName) {
    printf("STACK OVERFLOW: %s\n", pcTaskName);
    Error_Handler();
}

// Malloc failed hook
void vApplicationMallocFailedHook(void) {
    printf("MALLOC FAILED\n");
    Error_Handler();
}
```

## Task Notifications (Lightweight Alternative)

```c
TaskHandle_t xWorkerTaskHandle;

// ISR notifies task (faster than semaphore)
void EXTI_IRQHandler(void) {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    // Send notification with value
    xTaskNotifyFromISR(xWorkerTaskHandle, 0x01, eSetBits, &xHigherPriorityTaskWoken);

    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}

// Task waits for notification
void vWorkerTask(void *pvParameters) {
    uint32_t ulNotificationValue;

    for (;;) {
        // Wait for notification (replaces semaphore)
        if (xTaskNotifyWait(0x00, 0xFFFFFFFF, &ulNotificationValue, portMAX_DELAY) == pdTRUE) {
            // Handle event based on notification value
            HandleEvent(ulNotificationValue);
        }
    }
}
```

## Best Practices

- Use `vTaskDelayUntil()` for periodic tasks (prevents drift)
- Keep ISRs short - defer work to tasks via queues/semaphores
- Size stacks appropriately (monitor with `uxTaskGetStackHighWaterMark()`)
- Use task notifications instead of semaphores when possible (lower overhead)
- Protect shared resources with mutexes, not critical sections (unless very short)
- Configure watchdog for production builds
- Monitor heap usage to prevent fragmentation
- Use priority inheritance mutexes to avoid priority inversion
