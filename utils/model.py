import tensorflow as tf

class Recommender:
    def __init__(self):
        self.model = tf.keras.models.load_model('model')
    
    def get_recommendations(self, user_id):
        user_input = tf.constant([user_id])
        recommended_items = self.model(user_input)
        return [item.decode('utf-8') for item in recommended_items[1].numpy()[0].tolist()]

if __name__ == '__main__':
    # Path to the pre-trained model
    # Create an instance of the Recommender class
    rec = Recommender()
    # User ID for which to get recommendations
    user_id = "1"
    # Get recommendations
    predictions = rec.get_recommendations(user_id)
    # Print the predictions
    print(predictions)