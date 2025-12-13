import type { Episode } from '../types';

export const episodes: Episode[] = [
    {
        id: 1,
        title: "Meeting Someone New",
        description: "Learn how to introduce yourself and make small talk when meeting someone for the first time.",
        audioUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        transcript: {
            dialogue: [
                { speaker: "A", text: "Hi! I'm Sarah. Nice to meet you!" },
                { speaker: "B", text: "Hello Sarah! I'm John. Nice to meet you too!" },
                { speaker: "A", text: "So, what do you do for a living?" },
                { speaker: "B", text: "I'm a software engineer. How about you?" },
                { speaker: "A", text: "I work in marketing. It's quite interesting!" },
                { speaker: "B", text: "That sounds great! How long have you been in marketing?" },
                { speaker: "A", text: "About five years now. I really enjoy it." },
            ],
            vocabulary: [
                { word: "introduce", definition: "to tell someone another person's name for the first time" },
                { word: "small talk", definition: "polite conversation about unimportant or uncontroversial matters" },
                { word: "for a living", definition: "as a job or profession" },
            ]
        }
    },
    {
        id: 2,
        title: "Calling In Sick",
        description: "Learn the proper way to call your workplace when you're too ill to come to work.",
        audioUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        transcript: {
            dialogue: [
                { speaker: "Employee", text: "Good morning, this is Tom speaking." },
                { speaker: "Manager", text: "Hi Tom, this is Linda. How are you?" },
                { speaker: "Employee", text: "Actually, I'm not feeling well today. I think I have the flu." },
                { speaker: "Manager", text: "Oh no! I'm sorry to hear that. Do you need to take the day off?" },
                { speaker: "Employee", text: "Yes, I'm afraid so. I can barely get out of bed." },
                { speaker: "Manager", text: "That's fine. Take care of yourself and get some rest." },
                { speaker: "Employee", text: "Thank you for understanding. I'll keep you updated." },
            ],
            vocabulary: [
                { word: "call in sick", definition: "to telephone your workplace to say you are too ill to come to work" },
                { word: "the flu", definition: "a common infectious illness that causes fever and headache" },
                { word: "take the day off", definition: "to not go to work for a day" },
                { word: "barely", definition: "only just; almost not" },
            ]
        }
    },
    {
        id: 3,
        title: "Ordering at a Restaurant",
        description: "Master the vocabulary and phrases needed to order food at a restaurant confidently.",
        audioUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        transcript: {
            dialogue: [
                { speaker: "Waiter", text: "Good evening! Are you ready to order?" },
                { speaker: "Customer", text: "Yes, I'd like to start with the Caesar salad, please." },
                { speaker: "Waiter", text: "Excellent choice! And for your main course?" },
                { speaker: "Customer", text: "I'll have the grilled salmon with vegetables." },
                { speaker: "Waiter", text: "How would you like that cooked?" },
                { speaker: "Customer", text: "Medium, please." },
                { speaker: "Waiter", text: "Perfect! Anything to drink?" },
                { speaker: "Customer", text: "Just water, thank you." },
            ],
            vocabulary: [
                { word: "order", definition: "to ask for food or drink in a restaurant" },
                { word: "main course", definition: "the largest or most important part of a meal" },
                { word: "grilled", definition: "cooked over direct heat" },
                { word: "medium", definition: "cooked to a moderate degree (for meat)" },
            ]
        }
    },
    {
        id: 4,
        title: "Making a Doctor's Appointment",
        description: "Learn how to schedule a medical appointment over the phone professionally.",
        audioUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
        transcript: {
            dialogue: [
                { speaker: "Receptionist", text: "Dr. Smith's office, how may I help you?" },
                { speaker: "Patient", text: "Hi, I'd like to make an appointment with Dr. Smith." },
                { speaker: "Receptionist", text: "Of course! What's the reason for your visit?" },
                { speaker: "Patient", text: "I've been having headaches for the past week." },
                { speaker: "Receptionist", text: "I see. How about next Tuesday at 2 PM?" },
                { speaker: "Patient", text: "That works perfectly. Thank you!" },
                { speaker: "Receptionist", text: "Great! May I have your name and phone number?" },
            ],
            vocabulary: [
                { word: "appointment", definition: "an arrangement to meet someone at a particular time" },
                { word: "receptionist", definition: "a person who greets visitors and answers the phone" },
                { word: "headache", definition: "a continuous pain in the head" },
                { word: "works perfectly", definition: "is suitable or convenient" },
            ]
        }
    },
    {
        id: 5,
        title: "Asking for Directions",
        description: "Practice asking for and giving directions in English with common phrases and vocabulary.",
        audioUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
        transcript: {
            dialogue: [
                { speaker: "Tourist", text: "Excuse me, could you help me? I'm looking for the train station." },
                { speaker: "Local", text: "Sure! Go straight down this street for two blocks." },
                { speaker: "Tourist", text: "Okay, straight for two blocks..." },
                { speaker: "Local", text: "Then turn left at the traffic light. You'll see it on your right." },
                { speaker: "Tourist", text: "Turn left at the light, then it's on the right. Got it!" },
                { speaker: "Local", text: "It's about a five-minute walk from here." },
                { speaker: "Tourist", text: "Thank you so much for your help!" },
            ],
            vocabulary: [
                { word: "directions", definition: "instructions about how to get to a place" },
                { word: "block", definition: "the distance along a street from one cross street to the next" },
                { word: "traffic light", definition: "a signal that controls traffic at intersections" },
                { word: "got it", definition: "I understand" },
            ]
        }
    },
    {
        id: 6,
        title: "Job Interview Basics",
        description: "Essential phrases and etiquette for succeeding in your first English job interview.",
        audioUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
        transcript: {
            dialogue: [
                { speaker: "Interviewer", text: "Please, have a seat. Tell me about yourself." },
                { speaker: "Candidate", text: "Thank you. I'm a recent graduate with a degree in Computer Science." },
                { speaker: "Interviewer", text: "What interests you about this position?" },
                { speaker: "Candidate", text: "I'm passionate about web development and your company's innovative projects." },
                { speaker: "Interviewer", text: "What are your greatest strengths?" },
                { speaker: "Candidate", text: "I'm a quick learner and I work well in team environments." },
                { speaker: "Interviewer", text: "Do you have any questions for me?" },
                { speaker: "Candidate", text: "Yes, what does a typical day look like in this role?" },
            ],
            vocabulary: [
                { word: "candidate", definition: "a person applying for a job" },
                { word: "passionate", definition: "having strong feelings or beliefs about something" },
                { word: "strengths", definition: "good qualities or abilities" },
                { word: "typical", definition: "showing the usual characteristics" },
            ]
        }
    },
    {
        id: 7,
        title: "Shopping for Clothes",
        description: "Learn vocabulary and phrases for shopping at clothing stores and asking about sizes.",
        audioUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3",
        transcript: {
            dialogue: [
                { speaker: "Sales Assistant", text: "Hi! Can I help you find anything today?" },
                { speaker: "Customer", text: "Yes, I'm looking for a blue shirt." },
                { speaker: "Sales Assistant", text: "What size do you wear?" },
                { speaker: "Customer", text: "I'm usually a medium. Can I try this one on?" },
                { speaker: "Sales Assistant", text: "Of course! The fitting rooms are right over there." },
                { speaker: "Customer", text: "Thank you! Do you have this in any other colors?" },
                { speaker: "Sales Assistant", text: "Yes, we have it in white, black, and gray as well." },
            ],
            vocabulary: [
                { word: "size", definition: "how large or small something is" },
                { word: "try on", definition: "to put on clothing to see if it fits" },
                { word: "fitting room", definition: "a room where you can try on clothes in a store" },
                { word: "as well", definition: "also; too" },
            ]
        }
    },
    {
        id: 8,
        title: "Booking a Hotel Room",
        description: "Practice making hotel reservations and asking about amenities over the phone.",
        audioUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
        transcript: {
            dialogue: [
                { speaker: "Receptionist", text: "Grand Hotel, how may I assist you?" },
                { speaker: "Guest", text: "I'd like to book a room for next weekend, please." },
                { speaker: "Receptionist", text: "Certainly! For how many nights?" },
                { speaker: "Guest", text: "Two nights, Friday and Saturday." },
                { speaker: "Receptionist", text: "Would you prefer a single or double room?" },
                { speaker: "Guest", text: "A double room, please. Does it include breakfast?" },
                { speaker: "Receptionist", text: "Yes, breakfast is included in the rate." },
            ],
            vocabulary: [
                { word: "book", definition: "to reserve or arrange in advance" },
                { word: "amenities", definition: "features that provide comfort or convenience" },
                { word: "single room", definition: "a hotel room for one person" },
                { word: "rate", definition: "the price or cost" },
            ]
        }
    },
    {
        id: 9,
        title: "At the Bank",
        description: "Essential banking vocabulary for opening accounts and making transactions.",
        audioUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
        transcript: {
            dialogue: [
                { speaker: "Teller", text: "Good afternoon! How can I help you today?" },
                { speaker: "Customer", text: "I'd like to open a savings account." },
                { speaker: "Teller", text: "Great! Do you have a valid ID with you?" },
                { speaker: "Customer", text: "Yes, here's my driver's license." },
                { speaker: "Teller", text: "Perfect. What's your initial deposit amount?" },
                { speaker: "Customer", text: "I'd like to deposit $500." },
                { speaker: "Teller", text: "Excellent. I'll get the paperwork started for you." },
            ],
            vocabulary: [
                { word: "savings account", definition: "a bank account that earns interest" },
                { word: "valid ID", definition: "an official document that proves identity" },
                { word: "deposit", definition: "to put money into a bank account" },
                { word: "paperwork", definition: "documents that need to be completed" },
            ]
        }
    },
    {
        id: 10,
        title: "Talking About the Weather",
        description: "Common expressions and vocabulary for discussing weather conditions.",
        audioUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3",
        transcript: {
            dialogue: [
                { speaker: "A", text: "Beautiful day today, isn't it?" },
                { speaker: "B", text: "Yes! The weather has been lovely all week." },
                { speaker: "A", text: "I heard it might rain tomorrow though." },
                { speaker: "B", text: "Really? I hope not. I have outdoor plans." },
                { speaker: "A", text: "You should check the forecast just in case." },
                { speaker: "B", text: "Good idea. I'll bring an umbrella to be safe." },
                { speaker: "A", text: "Better safe than sorry!" },
            ],
            vocabulary: [
                { word: "lovely", definition: "very pleasant or beautiful" },
                { word: "forecast", definition: "a prediction of future weather" },
                { word: "just in case", definition: "as a precaution" },
                { word: "better safe than sorry", definition: "it's better to be careful than to regret not being careful" },
            ]
        }
    }
];
