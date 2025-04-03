import unittest
from digit_recognition.model import predict_digit, preprocess_image, create_visualization, save_to_base64, layer_visualization, visualize_feature_maps

class TestModel(unittest.TestCase):
    
    def test_digit_recognition(self):
        result_1 = predict_digit('./development/test_images/2.png')
        
        #check prediction
        self.assertEqual(result_1[0],2)
        
        #confidence
        self.assertEqual(result_1[1],99.999985)
        
        #response length
        self.assertEqual(len(result_1),5)
        
        #numbers of feature maps 
        self.assertEqual(len(result_1[4]),8)

unittest.main()