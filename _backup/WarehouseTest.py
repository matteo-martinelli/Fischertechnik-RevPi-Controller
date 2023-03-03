import unittest

from Warehouse import Warehouse
from WarehouseConfig import WarehouseConfig


class MyTestCase(unittest.TestCase):

    def setUp(self):
        #counterVertical,counterHorizontal,armEndIn,armEndOut,conveyorIn,conveyorOut,horizontalEnd,verticalEnd
        warehouseLoadConf1 = WarehouseConfig(1500,30,True,False,False,False,False,False) #mit eingefahrenem Arm in Ladepos
        warehouseLoadConf2 = WarehouseConfig(1500,30,False,True,False,False,False,False) #Arm ausfahren
        warehouseLoadConf3 = WarehouseConfig(1500,30,False,True,True,False,False,False) #Förderband aktivieren
        warehouseLoadConf4 = WarehouseConfig(1000,30,False,True,False,False,False,False) #anheben

        self.warehouse1 = Warehouse(1)

    def testGoToLoadConfigAfterSetup(self):
        self.warehouse1.warehouseSensVerticalEnd = True
        #execute
        self.warehouse1.execute()
        self.assertEqual(self.warehouse1.warehouseActVerticalUp, False)
        self.assertEqual(self.warehouse1.warehouseActVerticalDown, False)
        self.assertEqual(self.warehouse1.warehouseActHorizontalToRack, False)
        self.assertEqual(self.warehouse1.warehouseActHorizontalToConveyor, False)
        self.assertEqual(self.warehouse1.warehouseActArmIn, True)
        self.warehouse1.warehouseSensArmIn = True
        #execute
        self.warehouse1.execute()
        self.assertEqual(self.warehouse1.warehouseActVerticalUp, False)
        self.assertEqual(self.warehouse1.warehouseActVerticalDown, False)
        self.assertEqual(self.warehouse1.warehouseActHorizontalToRack, False)
        self.assertEqual(self.warehouse1.warehouseActHorizontalToConveyor, True)
        self.assertEqual(self.warehouse1.warehouseActArmIn, False)
        self.warehouse1.warehouseSensHorizontalEnd = True
        #execute
        self.warehouse1.execute()
        self.assertEqual(self.warehouse1.warehouseActVerticalUp, False)
        self.assertEqual(self.warehouse1.warehouseActVerticalDown, False)
        self.assertEqual(self.warehouse1.warehouseActHorizontalToRack, False)
        self.assertEqual(self.warehouse1.warehouseActHorizontalToConveyor, False)
        self.assertEqual(self.warehouse1.warehouseActArmIn, False)
        self.assertEqual(self.warehouse1.setupFinished, True)
        self.assertEqual(self.warehouse1.configReached, True)
        #execute
        self.warehouse1.execute() #ab hier folgt ausführung den configs
        #execute
        self.warehouse1.execute()
        self.assertEqual(self.warehouse1.warehouseActArmIn, False)
        self.assertEqual(self.warehouse1.warehouseActVerticalDown, True)
        self.assertEqual(self.warehouse1.warehouseActHorizontalToRack, True)
        self.warehouse1.warehouseSensEncoderVertical = 100
        #self.warehouse1.warehouseSensEncoderHorizontal = 30
        #execute
        self.warehouse1.execute()
        self.assertEqual(self.warehouse1.warehouseActArmIn, False)
        self.assertEqual(self.warehouse1.warehouseActVerticalDown, True)
        self.assertEqual(self.warehouse1.warehouseActHorizontalToRack, True)
        self.warehouse1.warehouseSensEncoderVertical = 1500
        self.warehouse1.warehouseSensEncoderHorizontal = 30
        #execute
        self.warehouse1.execute()
        self.assertEqual(self.warehouse1.warehouseActVerticalDown, False)
        self.assertEqual(self.warehouse1.warehouseActHorizontalToRack, False)
        #config1 reached
        #execute - Arm ausfahren
        self.warehouse1.execute()
        self.assertEqual(self.warehouse1.warehouseActArmOut, True)
        self.assertEqual(self.warehouse1.warehouseActVerticalDown, False)
        self.assertEqual(self.warehouse1.warehouseActHorizontalToRack, False)
        #execute
        self.warehouse1.execute()
        self.assertEqual(self.warehouse1.warehouseActArmOut, True)
        self.assertEqual(self.warehouse1.warehouseActVerticalDown, False)
        self.assertEqual(self.warehouse1.warehouseActHorizontalToRack, False)
        self.warehouse1.warehouseSensArmOut = True
        #execute
        self.warehouse1.execute()
        self.assertEqual(self.warehouse1.warehouseActArmOut, False)
        self.assertEqual(self.warehouse1.warehouseActVerticalDown, False)
        self.assertEqual(self.warehouse1.warehouseActHorizontalToRack, False)
        #config2 reached
        #execute - Förderband aktivieren
        self.warehouse1.execute()
        self.assertEqual(self.warehouse1.warehouseActArmIn, False)
        self.assertEqual(self.warehouse1.warehouseActVerticalDown, False)
        self.assertEqual(self.warehouse1.warehouseActHorizontalToRack, False)
        self.assertEqual(self.warehouse1.warehouseActConveyorIn, True)
        #execute
        self.warehouse1.execute()




if __name__ == '__main__':
    unittest.main()
