I started by outlining the logic of load_data in psudocode script. I implemented, tested, and checked it successfully. Then I moved on to implement the get_model() function. 

It was very confusing at first. After researching the TensorFlow docs, and correcting some misunderstanding, I decided to start with the simplest model possible. 

    1. Create Sequential model
    2. Flatten
    3. Output NUM_CATEGORIES nodes
    4. Compile model.

After a trial and error process of bug fixes, I got it to work! It performed poorly (low accuracy), but it ran error-free so I could experiment.

First I added a convolutional layer learning with a filter range starting 16 through 64, using a 3x3 kernel. It didn't seem to make much difference in terms of accuracy. 

Then I added a MaxPooling layer, which also didn't seem to make much difference. Maybe it optamizes the training time, I thought to myself. 

After adding a hidden layer with 16-128 nodes, and also changing the output activiation function from "Relu" to "Softmax" (and understanding why), the accuracy made significant improvement in accuracy. 

FInally I added dropout to guard against overfitting. 