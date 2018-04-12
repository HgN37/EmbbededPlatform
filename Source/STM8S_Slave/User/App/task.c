#include "task.h"
#include <stdlib.h>
#include <string.h>

//#define SLAVE_RELAY
#define SLAVE_LIGHT

frame_t frameTx;
frame_t frameRx;
uint8_t debug = 0;
uint16_t debug2 = 0;

void taskInit(void) {
    //! Set clock 16MHz
    CLK_HSICmd(ENABLE);
    CLK_HSIPrescalerConfig(CLK_PRESCALER_HSIDIV1);
    CLK_SYSCLKConfig(CLK_PRESCALER_CPUDIV1);
    CLK_AdjustHSICalibrationValue(CLK_HSITRIMVALUE_0);

    //! Init serial, ticker
    serialInit();
    tickerInit();
    enableInterrupts();
    tickerDelayMs(500);

    //! Init led
    ledInit(LED_1);

    //! Init random
    randomInit();

    //! Clear serial frame
    serialClearFrame(&frameTx);
    serialClearFrame(&frameRx);

    regInit();

    // Unactive addr = 0
    regWrite(REG_ADDR, 0x00);
    regWrite(REG_STATUS, randomGenerate()%32);
    randomDeInit();

#ifdef SLAVE_RELAY
    deviceInit(DEVICE_1);
    deviceOff(DEVICE_1);
    debug = deviceRead(DEVICE_1);
#endif
#ifdef SLAVE_LIGHT
    bh1750Init();
#endif

    // Hardware reg
#ifdef SLAVE_RELAY
    regWrite(REG_HARDWARE, 0x01);
    regWrite(REG_ID, 0x01);
#endif
#ifdef SLAVE_LIGHT
    regWrite(REG_HARDWARE, 0x05);
    regWrite(REG_ID, 0x01);
#endif

}

bool taskActivate(void) {
    //debug2 = bh1750Read();
    if(EXIT_SUCCESS != serialGetFrame(&frameRx)) {
        serialClearFrame(&frameTx);
        serialClearFrame(&frameRx);
        return false;
    }
    if(frameRx.addr != regRead(REG_ADDR)) {
        return false;
    }
    if(frameRx.func != SERIAL_FUNC_ACTIVE) {
        return false;
    }
    if(frameRx.num != 2) {
        return false;
    }
    if(frameRx.data[0] != regRead(REG_STATUS)) {
        return false;
    }
    regWrite(REG_ADDR, frameRx.data[1]);
    // Send respond
    frameTx.addr = regRead(REG_ADDR);
    frameTx.func = frameRx.func;
    frameTx.num = 2;
    frameTx.data = (uint8_t*)malloc(frameTx.num);
    frameTx.data[0] = regRead(REG_HARDWARE);
    frameTx.data[1] = regRead(REG_ID);
    serialSendFrame(&frameTx);
    serialClearFrame(&frameTx);
    serialClearFrame(&frameRx);
    return true;
}

void taskSerialCmd(void) {
    uint8_t count;
    if(EXIT_SUCCESS != serialGetFrame(&frameRx)) {
        serialClearFrame(&frameTx);
        serialClearFrame(&frameRx);
        return;
    }
    //! Check Addr
    if(frameRx.addr != regRead(REG_ADDR)) {
        serialClearFrame(&frameTx);
        serialClearFrame(&frameRx);
        return;
    }
    debug2++;
    //! Get function
    if(frameRx.func == SERIAL_FUNC_READ) {
        frameTx.addr = frameRx.addr;
        frameTx.func = frameRx.func;
        frameTx.num = frameRx.num;
        frameTx.data = (uint8_t*)malloc(frameTx.num);
        for(count = 0; count < frameRx.num; count++) {
            frameTx.data[count] = regRead(frameRx.reg + count);
        }
    }
    else if(frameRx.func == SERIAL_FUNC_WRITE) {
        frameTx.addr = frameRx.addr;
        frameTx.func = frameRx.func;
        frameTx.num = frameRx.num;
        frameTx.data = (uint8_t*)malloc(frameTx.num);
        for(count = 0; count < frameRx.num; count++) {
            regWrite(frameRx.reg + count, frameRx.data[count]);
        }
        taskReg2Dev();
        taskDev2Reg();
        for(count = 0; count < frameRx.num; count++) {
            frameTx.data[count] = regRead(frameRx.reg + count);
        }
    }
    serialSendFrame(&frameTx);
    serialClearFrame(&frameTx);
    serialClearFrame(&frameRx);
}

void taskReg2Dev(void) {
#ifdef SLAVE_RELAY
    if(regRead(0x11) == 0x64) {
        deviceOn(DEVICE_1);
    }
    else if(regRead(0x11) == 0x00) {
        deviceOff(DEVICE_1);
    }
    //tickerDelayMs(1);
#endif
#ifdef SLAVE_LIGHT
#endif
}

void taskDev2Reg(void) {
#ifdef SLAVE_RELAY
    //! Update relay status
    uint8_t stt;
    stt = deviceRead(DEVICE_1);
    if(stt == GPIO_LOW) {
        regWrite(0x10, 0x00);
        regWrite(0x11, 0x64);
    }
    else {
        regWrite(0x10, 0x00);
        regWrite(0x11, 0x00);
    }
#endif
#ifdef SLAVE_LIGHT
    uint16_t lux;
    lux = bh1750Read();
    regWrite(0x10, (uint8_t)(lux>>8));
    regWrite(0x11, (uint8_t)(lux));
#endif
}