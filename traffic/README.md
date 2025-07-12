I started by outlining the logic of load_data in psudocode script. I implemented, tested, and checked it successfully. Then I moved on to implement the get_model() function. 

It was very confusing at first. After researching the TensorFlow docs, and correcting some misunderstanding, I decided to start with the simplest model possible. 

    1. Create Sequential model
    2. Flatten
    3. Output NUM_CATEGORIES nodes
    4. Compile model.

After a trial and error process of bug fixes, I got it to work! It performed poorly (low accuracy), but it ran error-free so I could experiment.