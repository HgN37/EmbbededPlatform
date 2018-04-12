#include "bh1750.h"

/* Private Function */
void bh1750Delay(uint16_t nCount);

void bh1750Init(void)
{
    CLK_PeripheralClockConfig(CLK_PERIPHERAL_I2C, ENABLE);
    I2C_DeInit();
    I2C_Cmd( ENABLE);
    I2C_Init(100000, 0xA0, I2C_DUTYCYCLE_2, I2C_ACK_CURR, I2C_ADDMODE_7BIT, CLK_GetClockFreq()/1000000);
}

uint16_t bh1750Read(void)
{
    //uint8_t data_high, data_low;
    uint16_t data;
    uint8_t data_low, data_high;
    while(I2C_GetFlagStatus( I2C_FLAG_BUSBUSY)==SET);
    I2C_GenerateSTART(ENABLE);
    while(!I2C_CheckEvent( I2C_EVENT_MASTER_MODE_SELECT));
    I2C_Send7bitAddress(0x46,I2C_DIRECTION_TX);
    while(!I2C_CheckEvent( I2C_EVENT_MASTER_TRANSMITTER_MODE_SELECTED));
    I2C_SendData(0x01);
    while(I2C_GetFlagStatus(I2C_FLAG_TRANSFERFINISHED) == RESET);
    I2C_GenerateSTART( ENABLE);
    while(!I2C_CheckEvent( I2C_EVENT_MASTER_MODE_SELECT));
    I2C_Send7bitAddress(0x46,I2C_DIRECTION_TX);
    while(!I2C_CheckEvent( I2C_EVENT_MASTER_TRANSMITTER_MODE_SELECTED));
    I2C_SendData(0x07);
    while(I2C_GetFlagStatus(I2C_FLAG_TRANSFERFINISHED) == RESET);
    I2C->SR1;        I2C->SR3;
    I2C_GenerateSTOP(ENABLE);

    I2C_GenerateSTART( ENABLE);
    while(!I2C_CheckEvent( I2C_EVENT_MASTER_MODE_SELECT));
    I2C_Send7bitAddress(0x46,I2C_DIRECTION_TX);
    while(!I2C_CheckEvent( I2C_EVENT_MASTER_TRANSMITTER_MODE_SELECTED));
    I2C_SendData(0x20);
    while(I2C_GetFlagStatus(I2C_FLAG_TRANSFERFINISHED) == RESET);
    tickerDelayMs(300);
    I2C_GenerateSTART( ENABLE);
    while(!I2C_CheckEvent( I2C_EVENT_MASTER_MODE_SELECT));
    I2C_Send7bitAddress(0x46,I2C_DIRECTION_RX);
    while (I2C_GetLastEvent() != I2C_EVENT_MASTER_RECEIVER_MODE_SELECTED);
    I2C->SR1;        I2C->SR3;
    while (I2C_GetFlagStatus( I2C_FLAG_RXNOTEMPTY) == RESET);
    data_high=I2C_ReceiveData();
    data = (uint16_t)data_high << 8;
    while (I2C_GetFlagStatus( I2C_FLAG_RXNOTEMPTY) == RESET);
    data_low=I2C_ReceiveData();
    data = data | (uint16_t)data_low;
    I2C_GenerateSTOP(ENABLE);
    while(I2C->CR2 & I2C_CR2_STOP);
    return data;
}

void bh1750Delay(uint16_t nCount)
{
  /* Decrement nCount value */
  while (nCount != 0)
  {
    nCount--;
  }
}