#ifndef TASK_H
#define TASK_H

#include "protocol.h"
#include "reg.h"
#include "led.h"
#include "device.h"
#include "button.h"
#include "ds18b20.h"
#include "ticker.h"
#include "defineApp.h"
#include "random.h"
#include "i2c.h"
#include "bh1750.h"

void taskInit(void);
bool taskActivate(void);
void taskSerialCmd(void);
void taskReg2Dev(void);
void taskDev2Reg(void);

#endif