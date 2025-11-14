{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNaQudzGKrYVOuE0swg395F",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/KalebParsons/RCGT3Car/blob/main/Car_Code.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 2,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "collapsed": true,
        "id": "BbmkQqVw5Gzs",
        "outputId": "d9a06b27-9ac3-4132-c444-8150750ea92e"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Collecting evdev\n",
            "  Downloading evdev-1.9.2.tar.gz (33 kB)\n",
            "  Installing build dependencies ... \u001b[?25l\u001b[?25hdone\n",
            "  Getting requirements to build wheel ... \u001b[?25l\u001b[?25hdone\n",
            "  Preparing metadata (pyproject.toml) ... \u001b[?25l\u001b[?25hdone\n",
            "Building wheels for collected packages: evdev\n",
            "  Building wheel for evdev (pyproject.toml) ... \u001b[?25l\u001b[?25hdone\n",
            "  Created wheel for evdev: filename=evdev-1.9.2-cp312-cp312-linux_x86_64.whl size=113483 sha256=a36cda76618954eae9751a274b4647e99c361f3ae7512fe2e9cb18a641ecea4b\n",
            "  Stored in directory: /root/.cache/pip/wheels/19/f7/62/6b6f5201f6536a3a9e38c94726e03a3b2bded0aaf7782b12d7\n",
            "Successfully built evdev\n",
            "Installing collected packages: evdev\n",
            "Successfully installed evdev-1.9.2\n",
            "Collecting RPi.GPIO\n",
            "  Downloading RPi.GPIO-0.7.1.tar.gz (29 kB)\n",
            "  Preparing metadata (setup.py) ... \u001b[?25l\u001b[?25hdone\n",
            "Building wheels for collected packages: RPi.GPIO\n",
            "  Building wheel for RPi.GPIO (setup.py) ... \u001b[?25l\u001b[?25hdone\n",
            "  Created wheel for RPi.GPIO: filename=RPi.GPIO-0.7.1-cp312-cp312-linux_x86_64.whl size=72267 sha256=fbd7a31a9b5d4c99ad0d375add2688dce2265fbcd1344846cc4bff83b2ca2628\n",
            "  Stored in directory: /root/.cache/pip/wheels/63/75/4e/19132ca8a2e813e52c9e07f84ff41792d7a8ca70138e53c671\n",
            "Successfully built RPi.GPIO\n",
            "Installing collected packages: RPi.GPIO\n",
            "Successfully installed RPi.GPIO-0.7.1\n"
          ]
        }
      ],
      "source": [
        "!pip install evdev #We need to install evdev first as it does not come with the base python\n",
        "!pip install RPi.GPIO\n",
        "\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import evdev #Allows us to use a xbox coontroller.\n",
        "#We will ned evtest to test the functions of our controller once connected to the PI.\n",
        "import numpy as np\n",
        "import time\n",
        "\n",
        "try:\n",
        "    import RPi.GPIO as GPIO #This will allow us to confirgure certain pins on the raspberry pi for our applications.\n",
        "    print(\"RPi.GPIO imported successfully. Running on a Raspberry Pi.\")\n",
        "except RuntimeError:\n",
        "    print(\"RPi.GPIO import failed. Running in a non-Raspberry Pi environment (e.g., Colab). Using dummy GPIO.\")\n",
        "\n",
        "    class DummyGPIO:\n",
        "        BCM = \"BOARD\" # A placeholder for the mode, can be 'BCM' or 'BOARD'\n",
        "        OUT = \"OUT\" # A placeholder for output direction\n",
        "\n",
        "        def setmode(self, mode):\n",
        "            print(f\"Dummy GPIO: setmode({mode})\")\n",
        "\n",
        "        def setup(self, pin, direction):\n",
        "            print(f\"Dummy GPIO: setup(pin={pin}, direction={direction})\")\n",
        "\n",
        "        def output(self, pin, value):\n",
        "            print(f\"Dummy GPIO: output(pin={pin}, value={value})\")\n",
        "\n",
        "        def cleanup(self):\n",
        "            print(\"Dummy GPIO: cleanup()\")\n",
        "\n",
        "        class DummyPWM:\n",
        "            def __init__(self, pin, frequency):\n",
        "                self.pin = pin\n",
        "                self.frequency = frequency\n",
        "                print(f\"Dummy PWM: Initialized for pin {pin} at {frequency}Hz\")\n",
        "\n",
        "            def start(self, duty_cycle):\n",
        "                print(f\"Dummy PWM: Started with duty cycle {duty_cycle}%\")\n",
        "\n",
        "            def ChangeDutyCycle(self, duty_cycle):\n",
        "                print(f\"Dummy PWM: Changed duty cycle to {duty_cycle}%\")\n",
        "\n",
        "            def stop(self):\n",
        "                print(\"Dummy PWM: Stopped\")\n",
        "\n",
        "        def PWM(self, pin, frequency):\n",
        "            return self.DummyPWM(pin, frequency)\n",
        "\n",
        "    GPIO = DummyGPIO()\n",
        "#This code allows us to import GPIO. TRaditionally, collab which I am doing my coding on. does not allow\n",
        "#you to import GPIO. it will give you a name error. So this code allows us to bypass this issue and continue\n",
        "#to use collab and code.\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "collapsed": true,
        "id": "G4IZelGmAwN_",
        "outputId": "51036ce3-1e8d-46f5-d68f-9f57594f2982"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "RPi.GPIO import failed. Running in a non-Raspberry Pi environment (e.g., Colab). Using dummy GPIO.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Here will be where we begin to configure the pins of a raspberry pi to our DC motors.\n",
        "GPIO.setmode(GPIO.BCM)\n",
        "driveMotor_pwm = GPIO.PWM(18, 100)#23 represents the pin number and 100 represents the frequency\n",
        "driveMotor_pwm.start(0) #This starts our motor at speed 0. the motor is off.\n",
        "steerMotor_pwm = GPIO.PWM(23, 100)\n",
        "steerMotor_pwm.start(0)\n",
        "GPIO.setup(18, GPIO.OUT)\n",
        "GPIO.setup(23, GPIO.OUT)\n",
        "\n",
        "#Annotations can be found in the description file for this part.\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "collapsed": true,
        "id": "Y5pW0bVAb9IM",
        "outputId": "2945df49-09b9-4f22-bca0-541bcab75b8e"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Dummy GPIO: setmode(BOARD)\n",
            "Dummy PWM: Initialized for pin 18 at 100Hz\n",
            "Dummy PWM: Started with duty cycle 0%\n",
            "Dummy PWM: Initialized for pin 23 at 100Hz\n",
            "Dummy PWM: Started with duty cycle 0%\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "def forward(speed):\n",
        "  print(f\"going fowrad at speed{speed}%\")\n",
        "  GPIO.output(18, False)\n",
        "  driveMotor_pwm.ChangeDutyCycle(speed)\n",
        "  #changing the duty cycle tells us how much of the PWM cycle stays on. This allows us to modulate the power of the motors given the inputs of the\n",
        "  #controller. The frequency will stay fixed, but the length of the on and off wave change depending on the duty cycle.\n",
        "\n",
        "def backward(speed):\n",
        "  print(f\"going backward at speed{speed}%\")\n",
        "  GPIO.output(18, True)\n",
        "  driveMotor_pwm.ChangeDutyCycle(speed)\n",
        "\n",
        "def left(speed):\n",
        "  print(f\"turning left at speed{speed}%\")\n",
        "  GPIO.output(23, False)\n",
        "  steerMotor_pwm.ChangeDutyCycle(speed)\n",
        "\n",
        "def right(speed):\n",
        "  print(f\"turning right at speed{speed}%\")\n",
        "  GPIO.output(23, True)\n",
        "  steerMotor_pwm.ChangeDutyCycle(speed)"
      ],
      "metadata": {
        "id": "H_eJ4vwWa0Du"
      },
      "execution_count": 10,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#Test code to test our movement controls\n",
        "\n",
        "#Test forward\n",
        "forward(100)\n",
        "time.sleep(1) #Helps slow our program down for testing purposes. waits one second before moving to the next line of code.\n",
        "\n",
        "#test left:\n",
        "left(70)\n",
        "time.sleep(1)\n",
        "\n",
        "#test right:\n",
        "right(65)\n",
        "time.sleep(1)\n",
        "\n",
        "#test backward:\n",
        "backward(1)\n",
        "time.sleep(1)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "PcIotmWYm1MW",
        "outputId": "f20eb30d-ac4a-44ef-9593-c4a2d65cb70b"
      },
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "going fowrad at speed100%\n",
            "Dummy GPIO: output(pin=18, value=False)\n",
            "Dummy PWM: Changed duty cycle to 100%\n",
            "turning left at speed70%\n",
            "Dummy GPIO: output(pin=23, value=False)\n",
            "Dummy PWM: Changed duty cycle to 70%\n",
            "turning right at speed65%\n",
            "Dummy GPIO: output(pin=23, value=True)\n",
            "Dummy PWM: Changed duty cycle to 65%\n",
            "going backward at speed1%\n",
            "Dummy GPIO: output(pin=18, value=True)\n",
            "Dummy PWM: Changed duty cycle to 1%\n"
          ]
        }
      ]
    }
  ]
}