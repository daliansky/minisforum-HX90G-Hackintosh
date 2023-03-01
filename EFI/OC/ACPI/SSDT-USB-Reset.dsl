/*
 * Intel ACPI Component Architecture
 * AML/ASL+ Disassembler version 20210930 (64-bit version)
 * Copyright (c) 2000 - 2021 Intel Corporation
 * 
 * Disassembling to symbolic ASL+ operators
 *
 * Disassembly of /Users/sky/git/minisforum-HX90G-Hackintosh/EFI/OC/ACPI/SSDT-USB-Reset.aml, Tue Dec 27 14:09:46 2022
 *
 * Original Table Header:
 *     Signature        "SSDT"
 *     Length           0x0000010B (267)
 *     Revision         0x02
 *     Checksum         0x35
 *     OEM ID           "CORP"
 *     OEM Table ID     "UsbReset"
 *     OEM Revision     0x00001000 (4096)
 *     Compiler ID      "INTL"
 *     Compiler Version 0x20220331 (539099953)
 */
DefinitionBlock ("", "SSDT", 2, "CORP", "UsbReset", 0x00001000)
{
    External (_SB_.PCI0.GP17, DeviceObj)
    External (_SB_.PCI0.GP17.XHC0.RHUB, DeviceObj)
	External (_SB_.PCI0.GP17.XHC1.RHUB, DeviceObj)
    External (_SB_.PCI0.GP17.XHC1, DeviceObj)
    External (_SB_.PCI0.GP19.XHC2.RHUB, DeviceObj)
	External (_SB_.PCI0.GP19.XHC3.RHUB, DeviceObj)	
	External (_SB_.PCI0.GP19.XHC4.RHUB, DeviceObj)
	
    Scope (\_SB.PCI0.GP17.XHC0.RHUB)
    {
        Method (_STA, 0, NotSerialized)  // _STA: Status
        {
            If (_OSI ("Darwin"))
            {
                Return (Zero)
            }
            Else
            {
                Return (0x0F)
            }
        }
    }
	
	Scope (\_SB.PCI0.GP17.XHC1.RHUB)
    {
        Method (_STA, 0, NotSerialized)  // _STA: Status
        {
            If (_OSI ("Darwin"))
            {
                Return (Zero)
            }
            Else
            {
                Return (0x0F)
            }
        }
    }
	
	Scope (\_SB.PCI0.GP19.XHC2.RHUB)
    {
        Method (_STA, 0, NotSerialized)  // _STA: Status
        {
            If (_OSI ("Darwin"))
            {
                Return (Zero)
            }
            Else
            {
                Return (0x0F)
            }
        }
    }

	Scope (\_SB.PCI0.GP19.XHC3.RHUB)
    {
        Method (_STA, 0, NotSerialized)  // _STA: Status
        {
            If (_OSI ("Darwin"))
            {
                Return (Zero)
            }
            Else
            {
                Return (0x0F)
            }
        }
    }

	Scope (\_SB.PCI0.GP19.XHC4.RHUB)
    {
        Method (_STA, 0, NotSerialized)  // _STA: Status
        {
            If (_OSI ("Darwin"))
            {
                Return (Zero)
            }
            Else
            {
                Return (0x0F)
            }
        }
    }

    Scope (\_SB.PCI0.GP17.XHC1)
    {
        Method (_STA, 0, NotSerialized)  // _STA: Status
        {
            If (_OSI ("Darwin"))
            {
                Return (Zero)
            }
            Else
            {
                Return (0x0F)
            }
        }
    }

    Scope (\_SB.PCI0.GP17)
    {
        Device (XHC2)
        {
            Name (_ADR, 0x04)  // _ADR: Address
            Method (_STA, 0, NotSerialized)  // _STA: Status
            {
                If (_OSI ("Darwin"))
                {
                    Return (0x0F)
                }
                Else
                {
                    Return (Zero)
                }
            }
        }
    }
}

