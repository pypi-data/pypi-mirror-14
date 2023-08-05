from PyObjCTools.TestSupport import *

import AVFoundation

class TestAVAudioUnitDistortion (TestCase):
    @min_os_level('10.7')
    def testConstants(self):
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetDrumsBitBrush, 0)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetDrumsBufferBeats, 1)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetDrumsLoFi, 2)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiBrokenSpeaker, 3)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiCellphoneConcert, 4)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiDecimated1, 5)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiDecimated2, 6)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiDecimated3, 7)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiDecimated4, 8)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiDistortedFunk, 9)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiDistortedCubed, 10)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiDistortedSquared, 11)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiEcho1, 12)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiEcho2, 13)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiEchoTight1, 14)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiEchoTight2, 15)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetMultiEverythingIsBroken, 16)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetSpeechAlienChatter, 17)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetSpeechCosmicInterference, 18)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetSpeechGoldenPi, 19)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetSpeechRadioTower, 20)
        self.assertEqual(AVFoundation.AVAudioUnitDistortionPresetSpeechWaves, 21)


if __name__ == "__main__":
    main()
