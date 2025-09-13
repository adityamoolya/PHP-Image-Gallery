# Image Gallery Frontend - CloneFest 2025

A modern, responsive image gallery frontend built with Node.js and Express, designed to showcase posts and albums from the backend API.

## Features

- 🖼️ **Image Gallery**: Browse posts with beautiful grid layout
- 🎨 **Modern UI**: Clean, responsive design with smooth animations
- 🔍 **Search & Filter**: Search posts by title, caption, or alt text
- 📁 **Album Organization**: Filter posts by albums
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- ⚡ **Fast Loading**: Optimized images with lazy loading
- 🎯 **Modal View**: Full-screen image viewing with details
- 🔗 **Social Sharing**: Share posts with native sharing API

## Tech Stack

- **Backend**: Node.js + Express
- **Frontend**: Vanilla JavaScript (ES6+)
- **Styling**: Modern CSS with CSS Grid and Flexbox
- **Icons**: Font Awesome
- **Fonts**: Inter (Google Fonts)
- **Deployment**: Railway

## API Integration

The frontend integrates with the backend API at `https://dependable-manifestation-production-2bc6.up.railway.app`:

- **Posts**: `/api/posts` - Fetch posts with pagination and filtering
- **Albums**: `/api/albums` - Fetch available albums
- **Search**: Built-in search functionality across post content
- **Filtering**: Filter by albums and tags

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser to `http://localhost:3000`

### Production Deployment

1. Build the application:
   ```bash
   npm run build
   ```

2. Start the production server:
   ```bash
   npm start
   ```

## Railway Deployment

This application is configured for Railway deployment:

- **Procfile**: Defines the web process
- **runtime.txt**: Specifies Node.js version
- **package.json**: Includes all necessary dependencies

### Environment Variables

Set the following environment variable in Railway:

- `BACKEND_URL`: URL of the backend API (defaults to the provided Railway URL)

## Project Structure

```
frontend_final/
├── public/
│   ├── index.html          # Main HTML file
│   ├── src/
│   │   └── app.js          # Main JavaScript application
│   └── styles/
│       └── main.css        # Main stylesheet
├── server.js               # Express server
├── package.json            # Dependencies and scripts
├── Procfile               # Railway deployment config
├── runtime.txt            # Node.js version
└── README.md              # This file
```

## Features in Detail

### Image Gallery
- Responsive grid layout that adapts to screen size
- Hover effects with overlay actions
- Lazy loading for better performance
- Smooth transitions and animations

### Search & Filtering
- Real-time search across post titles, captions, and alt text
- Album-based filtering
- Tag-based filtering
- Pagination with "Load More" functionality

### Modal View
- Full-screen image viewing
- Post metadata display (author, date, views)
- Tag display
- Social sharing capabilities
- Keyboard navigation (ESC to close)

### Responsive Design
- Mobile-first approach
- Breakpoints for tablet and desktop
- Touch-friendly interface
- Optimized for all screen sizes

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance Optimizations

- Lazy loading of images
- Efficient API calls with pagination
- CSS animations with `prefers-reduced-motion` support
- Optimized bundle size
- CDN-hosted fonts and icons

## Accessibility

- Keyboard navigation support
- Screen reader friendly
- High contrast mode support
- Focus indicators
- Semantic HTML structure

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please contact the development team or create an issue in the repository.

---

Built with ❤️ for CloneFest 2025
