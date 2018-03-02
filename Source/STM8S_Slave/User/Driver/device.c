/*******************************************************************************
  * @filename   : device.c
  * @author     : HgN
  * @last update: December 11th, 2017
  */
/******************************************************************************/

/******************************************************************************/
/* INCLUDE */
/******************************************************************************/
#include "device.h"
#include <stdlib.h>

/******************************************************************************/
/* LOCAL TYPEDEFS */
/******************************************************************************/

/******************************************************************************/
/* LOCAL DEFINES */
/******************************************************************************/

/******************************************************************************/
/* PUBLIC VARIABLES */
/******************************************************************************/
uint16_t _devicePort[4] = {
    DEVICE_1_PORT,
    DEVICE_2_PORT,
    DEVICE_3_PORT,
    DEVICE_4_PORT
};

uint8_t _devicePin[4] = {
    DEVICE_1_PIN,
    DEVICE_2_PIN,
    DEVICE_3_PIN,
    DEVICE_4_PIN
};
/******************************************************************************/
/* LOCAL FUNCTION PROTOTYPES */
/******************************************************************************/

/******************************************************************************/
/* PUBLIC FUNCTIONS */
/******************************************************************************/
/**
 * @brief       Init device
 * @param       device number
 * @reval       None
 */
void deviceInit(uint8_t pdevice) {
    uint16_t vPort = _devicePort[pdevice];
    uint8_t vPin = _devicePin[pdevice];
    gpioPinMode(vPort, vPin, GPIO_OUTPUT);
    gpioWritePin(vPort, vPin, GPIO_HIGH);
}

/**
 * @brief       Turn device on
 * @param       device number
 * @reval       None
 */
void deviceOn(uint8_t pdevice) {
    uint16_t vPort = _devicePort[pdevice];
    uint8_t vPin = _devicePin[pdevice];
    gpioWritePin(vPort, vPin, GPIO_LOW);
}

/**
 * @brief       Turn device off
 * @param       device number
 * @reval       None
 */
void deviceOff(uint8_t pdevice) {
    uint16_t vPort = _devicePort[pdevice];
    uint8_t vPin = _devicePin[pdevice];
    gpioWritePin(vPort, vPin, GPIO_HIGH);
}
/**
 * @brief       Read device status
 * @param       Device number
 * @reval       GPIO_LOW/GPIO_HIGH
 */
uint8_t deviceRead(uint8_t pdevice) {
    uint16_t vPort = _devicePort[pdevice];
    uint8_t vPin = _devicePin[pdevice];
    return gpioReadPin(vPort, vPin);
}