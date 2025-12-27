# BJJ Flow Diagram

An interactive visual tool for exploring Brazilian Jiu-Jitsu positions, techniques, and transitions.

## 🥋 Overview

The BJJ Flow Diagram is an interactive web-based application that maps out the relationships between BJJ positions, submissions, escapes, passes, sweeps, and counters. Navigate through the interconnected web of techniques to understand how positions flow into each other and discover various attack and defense options.

## 👥 Intended Audience

This diagram is designed for:
- **Students**: Visual learning of technique relationships and positional concepts
- **Instructors**: Teaching tool for demonstrating position hierarchies and transitions
- **Competition Practitioners**: Understanding strategic position flows and counters
- **Curriculum Planners**: Mapping skill progressions from basic to advanced

Whether you're a beginner trying to understand the landscape of BJJ or an experienced practitioner refining your game, this tool provides a comprehensive visual reference for the art.

## ✨ Features

- **Interactive Diagram**: Click on any position or technique to view detailed information
- **11 Core Positions**: Mount, Side Control, Guard, Back Mount, Turtle, and more
- **70+ Techniques**: Detailed submissions, escapes, passes, sweeps, and takedowns
- **Counters**: Learn defensive techniques for submissions
- **Difficulty Filtering**: Toggle between Basic, Intermediate, and Advanced techniques
- **Category Filtering**: Show/hide specific categories (Escapes, Submissions, Sweeps, Passes, Takedowns, Counters)
- **Dynamic Layout**: Multi-column layout for easy navigation
- **Zoom & Pan**: Explore the full diagram with intuitive zoom controls
- **Detailed Instructions**: Step-by-step breakdowns, key points, and common mistakes

## 🎯 How to Use

### Navigation
- **Click on a Position**: View all techniques available from that position
- **Click on a Technique**: See detailed instructions, key points, and variations
- **Zoom Controls**: Use +/- buttons or mouse wheel to zoom
- **Pan**: Click and drag to move around the diagram
- **Reset View**: Click the ⟲ button to return to center

### Filtering
- **Difficulty Levels**: Toggle Basic, Intermediate, or Advanced techniques
- **Categories**: Show/hide specific technique types:
  - **Escapes** (Dark Teal): Getting out of bad positions
  - **Counters** (Medium Teal): Defending submissions
  - **Submissions** (Red): Finishing techniques
  - **Sweeps** (Orange): Reversals from bottom position
  - **Passes** (Light Blue): Getting past the guard
  - **Takedowns** (Yellow): Standing techniques

### Understanding the Layout
- **Center Column**: Positions (circles)
- **Left Side**: Escapes and Passes (defensive techniques)
- **Right Side**: Submissions, Sweeps, and Takedowns (offensive techniques)
- **Counter Columns**: Submission defenses appear to the left of submissions
- **Dynamic Positioning**: Techniques automatically adjust spacing based on visible filters
  - Positions vertically space based on technique density
  - Counter columns reserve space only when counters are visible
  - Multi-column layout (max 6 techniques per column) optimizes horizontal space
  - Smooth transitions when toggling filters

## 🔧 Technical Details

- **Built with**: D3.js for visualization, vanilla JavaScript
- **No dependencies**: Single HTML file, works offline
- **Responsive**: Works on desktop and tablet
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge)

### Dynamic Positioning System
The diagram uses an intelligent layout algorithm that automatically adjusts spacing based on content:
- **Multi-column layout**: Techniques are organized in columns with a maximum of 6 techniques per column
- **Category-based grouping**: Techniques are grouped by type (escapes, passes, submissions, sweeps, takedowns) and difficulty level
- **Dynamic spacing**: Position spacing adjusts automatically based on the number of visible techniques
- **Counter positioning**: Submission counters use overlap detection to position themselves adjacent to their parent techniques while avoiding conflicts
- **Smooth transitions**: 500ms animated transitions when filtering techniques by difficulty or category
- **Intelligent layout**: Counters reserve space dynamically - when toggled off, other techniques shift left to fill the space

## 🤝 Contributing

I want your feedback! Whether you've found a technique that should be added, spotted an error in the instructions, have suggestions for improving the layout, or ideas for new features - please share!

- Open an issue on GitHub
- Suggest techniques or corrections
- Report bugs or usability issues
- Propose new features

This tool is built for the community, and your input helps make it better for everyone.

## 📝 Note on Technique Descriptions

Techniques are presented as educational reference. Always practice under the supervision of a qualified instructor. BJJ involves physical contact and carries inherent risks.

## 🔄 Updates

**Current Version**: Contains 70+ core techniques across all positions with detailed instructions.

**Future Enhancements**:
- Video/GIF demonstrations
- User login and authentication
- Personal training notes for each technique
- Shared technique comments and community insights
- Additional techniques and counters

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

Thanks to everyone who has provided input and feedback!

---

*OSS* 🥋
