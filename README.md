# 📚 Better English Everyday - Master English Through Practice

A modern, interactive web application for mastering English through comprehensive audio lessons, vocabulary building, and conversation practice. Built with React, TypeScript, and Vite, featuring a beautiful responsive UI with light/dark theme support and mobile optimization.

![Better English Everyday Screenshot](https://via.placeholder.com/800x400?text=Better+English+Everyday)

## ✨ Features

### 🎨 Modern Design
- **Dual Theme Support**: Light, Dark, and System themes with smooth transitions
- **Responsive Layout**: Two-column design with episode list and player
- **Beautiful UI**: Modern aesthetics with gradients, shadows, and animations
- **Custom Scrollbars**: Styled scrollbars matching the theme

### 🎵 Audio Player
- **Full Playback Controls**: Play/Pause, Previous/Next
- **Skip Controls**: -10s and +10s buttons for quick navigation
- **Progress Bar**: Visual progress with clickable seek functionality
- **Speed Control**: Adjustable playback speed (0.5x to 2x)
- **Volume Control**: Interactive volume slider
- **Loop & Autoplay**: Toggle options for continuous learning
- **Time Display**: Current time and total duration

### 📚 Learning Features
- **Episode List**: 10 English learning episodes covering various topics
- **Searchable**: Filter episodes by title, description, or episode number
- **Transcripts**: Full dialogue transcripts with speaker labels
- **Vocabulary**: Key words and definitions for each episode
- **Toggle View**: Show/hide transcript and vocabulary sections

### 🎯 Topics Covered
1. Meeting Someone New
2. Calling In Sick
3. Ordering at a Restaurant
4. Making a Doctor's Appointment
5. Asking for Directions
6. Job Interview Basics
7. Shopping for Clothes
8. Booking a Hotel Room
9. At the Bank
10. Talking About the Weather

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ installed
- npm or yarn package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd podcast-for-newbie
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to:
```
http://localhost:5173
```

## 🛠️ Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **CSS3** - Styling with CSS variables for theming
- **HTML5 Audio API** - Audio playback

## 📁 Project Structure

```
src/
├── components/          # React components
│   ├── Header.tsx      # Header with theme switcher and search
│   ├── EpisodeList.tsx # Scrollable episode list
│   ├── EpisodeDetail.tsx # Episode details container
│   ├── AudioPlayer.tsx # Full-featured audio player
│   ├── Transcript.tsx  # Transcript and vocabulary display
│   └── Footer.tsx      # Footer with coffee link
├── hooks/              # Custom React hooks
│   ├── useTheme.ts    # Theme management hook
│   └── useAudioPlayer.ts # Audio player logic hook
├── data/               # Application data
│   └── episodes.ts    # Episode data with transcripts
├── types.ts           # TypeScript type definitions
├── App.tsx            # Main application component
├── main.tsx           # Application entry point
└── index.css          # Global styles and theme variables
```

## 🎨 Customization

### Adding New Episodes

Edit `src/data/episodes.ts` and add new episode objects:

```typescript
{
  id: 11,
  title: "Your Episode Title",
  description: "Episode description",
  audioUrl: "https://example.com/audio.mp3",
  transcript: {
    dialogue: [
      { speaker: "A", text: "Hello!" },
      { speaker: "B", text: "Hi there!" }
    ],
    vocabulary: [
      { word: "hello", definition: "a greeting" }
    ]
  }
}
```

### Customizing Colors

Edit CSS variables in `src/index.css`:

```css
:root {
  --accent-primary: #10b981;  /* Primary accent color */
  --accent-secondary: #6366f1; /* Secondary accent color */
  /* ... more variables */
}
```

## 🌐 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Opera (latest)

## 📝 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Inspired by [EnglishPod](https://huynhthientung.github.io/english-pod/)
- Audio samples from [SoundHelix](https://www.soundhelix.com/)
- Icons: Unicode emoji characters

## ☕ Support

If you find this project helpful, consider buying me a coffee!

---

**Built with ❤️ for English learners worldwide**
