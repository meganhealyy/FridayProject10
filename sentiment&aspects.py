import openai
import pandas as pd

# Your OpenAI API key
openai.api_key = 'key'

# List of relevant product aspects you want to focus on
relevant_aspects = ['quality', 'service', 'price', 'features', 'design', 'performance', 'material']

# Function to perform sentiment analysis
def analyze_sentiment(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can try "gpt-4" as well
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Analyze the sentiment of the following text: {text}"}
            ],
            temperature=0.3
        )

        sentiment = response['choices'][0]['message']['content'].strip().lower()

        # Classify sentiment
        if 'positive' in sentiment:
            return 'Positive'
        elif 'negative' in sentiment:
            return 'Negative'
        else:
            return 'Neutral'

    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return 'Error'


# Function to perform aspect extraction using basic string processing
def extract_aspects(text):
    # Convert the review to lowercase and split by spaces
    words = text.lower().split()

    # Find the relevant aspects based on the presence of predefined keywords
    aspects = [word for word in words if word in relevant_aspects]
    
    return aspects


# Function to process and analyze reviews
def analyze_reviews(reviews):
    # Lists to store sentiment and aspects
    sentiments = []
    aspects_list = []
    
    for review in reviews:
        sentiment = analyze_sentiment(review['Consumer Feedback'])
        aspects = extract_aspects(review['Consumer Feedback'])
        
        # Save sentiment
        sentiments.append(sentiment)
        
        # Save aspects (max 3 aspects per review, for example)
        aspects_list.append(aspects[:3])  # Limit to top 3 aspects

    # Add sentiment and aspects to the DataFrame
    return sentiments, aspects_list


# Example reviews data
reviews_data = [
    [1, "The immersive experience of the Apple Vision Pro is unlike anything I've tried before. However, the battery life doesn't last as long as I'd hoped, requiring frequent charging throughout the day."],
[2, 'I love the sleek design of the Vision Pro, and it fits comfortably even during extended use. The materials feel premium, and it definitely turns heads.'],
[3, 'The price tag of the Vision Pro is quite steep, making it hard to justify the investment for the average user. I wish there were a more affordable option with similar features.'],
[4, "Navigating through the interface feels intuitive, and the integration with other Apple devices is seamless. It's great how easily it syncs with my iPhone and MacBook."],
[5, 'I experienced some lag while running high-demand applications, which was disappointing for such a premium product. It interrupted my workflow and was quite frustrating.'],
[6, 'Customer service was incredibly helpful when I had trouble setting up the Vision Pro for the first time. They walked me through each step patiently until everything was working smoothly.'],
[7, "The Vision Pro's augmented reality features are impressive, bringing digital elements into the real world convincingly. However, the selection of compatible apps is still limited, which reduces its utility."],
[8, 'Wearing the headset for more than two hours becomes uncomfortable, as it puts pressure on my nose. I hope future versions will address the weight distribution better.'],
[9, 'I appreciate the high-quality build and materials used in the Vision Pro; it feels durable and premium. The attention to detail in its design is truly remarkable.'],
[10, "The setup process was a bit complicated and not as straightforward as other Apple products I've used. It took me a while to figure out the calibration settings."],
[11, 'The battery life is exceptional, allowing me to use the Vision Pro throughout the day without needing a recharge. This is perfect for long work sessions or extended entertainment.'],
[12, "I wish the Vision Pro was lighter; after a while, it starts to feel cumbersome. It's not ideal for long-term wear, especially during travel."],
[13, 'The display resolution is stunning, making every detail crisp and clear. Watching movies and viewing photos is an entirely new experience with this level of clarity.'],
[14, "I'm impressed with how smoothly the Vision Pro runs even the most demanding applications. Multitasking is a breeze, and I haven't encountered any performance issues."],
[15, 'I encountered some software glitches that required restarting the device, which interrupted my work. For the price, I expected a more stable software experience.'],
[16, 'The Vision Pro seamlessly syncs with my Mac and iPhone, enhancing my productivity. The continuity between devices makes it easy to pick up where I left off.'],
[17, "Considering its features, the Vision Pro offers good value for the money. It's an investment, but the functionality it provides justifies the cost for me."],
[18, "I was underwhelmed by the limited customization options available in the settings. I'd like more control over the user interface and features."],
[19, "The audio quality is immersive, making media consumption a joy on the Vision Pro. The spatial audio adds depth to movies and music that I've never experienced before."],
[20, "It's frustrating that some essential apps are not yet optimized for the Vision Pro. This limits its usefulness for my daily tasks."],
[21, "The Vision Pro's display is incredibly sharp, and the color accuracy is top-notch, making it perfect for creative work. However, I noticed some minor overheating during extended sessions."],
[22, 'I love how easy it is to switch between AR and VR modes. It feels natural and enhances productivity, but the learning curve for certain gestures was steeper than I expected.'],
[23, 'The headset is a game-changer for virtual meetings, making interactions feel much more personal. However, the price point makes it hard to recommend to everyone on my team.'],
[24, 'The build quality is excellent, but I wish the device had more padding around the face for added comfort. After a few hours, it starts to feel a bit tight.'],
[25, "The Vision Pro integrates perfectly with Apple services like iCloud and FaceTime. It's nice to see everything work together so seamlessly, as expected from Apple."],
[26, 'While the design is futuristic and sleek, the lack of adjustable straps for head sizes was a bit inconvenient. It took me a while to get a snug fit.'],
[27, "The Vision Pro's audio system is phenomenal, providing an immersive experience without the need for headphones. It’s one of the standout features for me."],
[28, "I'm amazed by the potential for productivity apps on this device, but the current app library feels underwhelming. I hope developers start rolling out more options soon."],
[29, "The Vision Pro's eye-tracking technology is incredibly accurate and makes navigation feel effortless. It's a glimpse into the future of user interfaces."],
[30, 'Battery life is a letdown for such a high-end device. I find myself tethered to a power bank more often than I’d like.'],
[31, "The initial setup was smooth, and the instructions were clear. It's one of the most user-friendly setups I've experienced with AR/VR products."],
[32, 'The Vision Pro shines when it comes to collaborative work, allowing multiple users to interact with virtual objects in real-time. This is a big win for teamwork.'],
[33, "For its price, I expected more storage capacity. The Vision Pro's internal storage fills up quickly, especially with high-res apps and media."],
[34, "The headset's weight distribution is better than most competitors, but it still gets tiring during extended use. Comfort could definitely be improved in future iterations."],
[35, 'The ability to use Vision Pro as an external monitor for my MacBook is a game-changer. It’s like having an ultra-wide display without the desk space.'],
[36, 'While the design is stunning, I wish it came in more color options. A bit of personalization would go a long way for a device like this.'],
[37, 'The Vision Pro is an amazing concept, but the price is out of reach for many consumers. If Apple made a more affordable version, it would be a hit.'],
[38, 'Performance is flawless, even when running graphically intense apps. I haven’t experienced any lag or stutters, which is impressive.'],
[39, 'Customer support was quick to respond when I had issues pairing my Vision Pro with my iPhone. Their guidance was excellent, as always with Apple.'],
[40, 'The Vision Pro is packed with features, but it feels like a product geared more toward early adopters and tech enthusiasts than the average consumer.'],
[41, 'The Vision Pro feels like an overpriced gadget rather than a necessary tool. For the cost, I expected a lot more functionality and fewer gimmicks.'],
[42, 'The weight of the device is a serious issue—it feels like a brick on my face after just 30 minutes. Comfort clearly wasn’t a priority in the design.'],
[43, 'The app selection is abysmal. For something so expensive, it’s shocking how little you can actually do with it right now.'],
[44, 'Battery life is pathetic. It barely lasts through a movie, which makes it feel like more of a toy than a practical device.'],
[45, 'I ran into compatibility issues with several apps that I use daily. For a device that’s supposed to ‘just work,’ this was incredibly frustrating.'],
[46, 'The Vision Pro’s price tag is laughable for what you get. There are more affordable alternatives that offer similar or even better features.'],
[47, 'Customer service was surprisingly unhelpful when I had an issue with the sensors not calibrating. It took weeks to resolve a problem that shouldn’t have occurred in the first place.'],
[48, 'The setup process was confusing and riddled with bugs. It’s not the seamless Apple experience I’ve come to expect.'],
[49, 'The Vision Pro overheats way too quickly, making it impossible to use for extended periods. For this price, thermal management should have been flawless.'],
[50, 'The eye-tracking is hit or miss, often misinterpreting where I’m looking. It ruins the whole experience when basic features don’t work properly.'],
[51, 'Comfort is a huge drawback—the headset feels bulky and awkward, making it hard to imagine anyone wearing it for long periods.'],
[52, 'The visuals are decent, but for the price, I expected groundbreaking clarity. It doesn’t live up to the hype Apple marketed.'],
[53, 'The Vision Pro relies too heavily on being part of the Apple ecosystem. If you don’t already own other Apple devices, its functionality is severely limited.'],
[54, 'The lack of physical controls is annoying. Sometimes the gestures don’t register properly, and I’m left fumbling around to perform simple tasks.'],
[55, 'For a device so expensive, the build quality doesn’t feel robust. It seems fragile, like it could break with one wrong move.'],
[56, 'The promised productivity features are underwhelming. It’s marketed as a tool for professionals, but it feels like a gimmick in practice.'],
[57, 'I’m disappointed with how heavy and cumbersome the Vision Pro feels. It’s not something I’d want to use regularly, let alone recommend to others.'],
[58, 'Software glitches are far too common. It crashes frequently, which completely ruins the user experience.'],
[59, 'The Vision Pro isn’t user-friendly at all. The controls feel unintuitive, and it doesn’t come close to the simplicity of other Apple products.'],
[60, 'The Vision Pro is a classic example of form over function. It looks great, but the actual experience of using it leaves much to be desired.'],
[61, 'The Vision Pro has some unique features, but it feels like a product that’s still finding its footing. It’s neither amazing nor terrible—just okay.'],
[62, 'The design is sleek, as expected from Apple, but the usability isn’t groundbreaking. It’s good for casual use, but nothing revolutionary.'],
[63, 'The battery life is average—it’s not the best I’ve seen, but it’s not the worst either. It gets the job done for most sessions.'],
[64, 'The setup process was relatively straightforward, though there were a few moments where I had to double-check the manual. It wasn’t difficult, just a bit time-consuming.'],
[65, 'The Vision Pro offers a decent AR experience, but the app library is still growing. It’s a solid start, but it feels like early days for the platform.'],
[66, 'The audio quality is clear and immersive, but it doesn’t stand out compared to other high-end devices. It’s good, but not exceptional.'],
[67, 'The price is undeniably high, but the quality matches Apple’s usual standard. Whether it’s worth it depends entirely on your needs.'],
[68, 'I’ve noticed a few minor bugs here and there, but nothing that completely ruins the experience. It’s not perfect, but it’s functional.'],
[69, 'The Vision Pro is a cool device for entertainment, but I’m not sure it’s a must-have. It feels more like a luxury item than a necessity.'],
[70, 'The weight is noticeable but manageable. It’s not the most comfortable headset I’ve worn, but it’s not unbearable either.'],
[71, 'The integration with the Apple ecosystem is convenient if you already own other Apple products. Otherwise, it doesn’t add much.'],
[72, 'The visuals are clear, but they don’t feel as revolutionary as the marketing suggests. It’s a step up from most devices but not a giant leap.'],
[73, 'Comfort is decent, though I wouldn’t recommend wearing it for extended periods. It’s fine for shorter sessions.'],
[74, 'The Vision Pro is a solid piece of hardware, but the software needs more polish. It’s usable, but there’s room for improvement.'],
[75, 'The eye-tracking is a nice feature, though I’ve had moments where it didn’t work as expected. It’s a mixed bag.'],
[76, 'The Vision Pro performs well overall, but it doesn’t excel in any particular area. It’s a jack-of-all-trades kind of device.'],
[77, 'Customer support was helpful when I had questions, though the wait time was a bit longer than I’d like. They eventually resolved my issue.'],
[78, 'The AR and VR features are interesting, but I’m not sure how much I’ll use them day-to-day. It feels more like a novelty than a necessity.'],
[79, 'The build quality is good, but it doesn’t feel significantly different from other premium devices. It’s solid, but not standout.'],
[80, 'The Vision Pro works as advertised, but it doesn’t blow me away. It’s a fine addition to the Apple lineup, but it’s not a game-changer.'],
]

# Create DataFrame from reviews data
feedback_df = pd.DataFrame(reviews_data)

# Perform sentiment analysis and aspect extraction
sentiments, aspects = analyze_reviews(reviews_data)

# Add results to DataFrame
feedback_df['Sentiment'] = sentiments
feedback_df['Aspect 1'] = [aspect[0] if len(aspect) > 0 else None for aspect in aspects]
feedback_df['Aspect 2'] = [aspect[1] if len(aspect) > 1 else None for aspect in aspects]
feedback_df['Aspect 3'] = [aspect[2] if len(aspect) > 2 else None for aspect in aspects]

# Save the DataFrame to an Excel file
feedback_df.to_excel('customer_feedback_with_sentiments_and_aspects.xlsx', index=False)

print("Data saved to customer_feedback_with_sentiments_and_aspects.xlsx")
