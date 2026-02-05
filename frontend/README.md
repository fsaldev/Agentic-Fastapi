# Rent a Car - Frontend

A modern frontend application for managing a car rental business built with Next.js 14, TypeScript, Tailwind CSS, and shadcn/ui.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **Icons**: Lucide React

## Getting Started

### Prerequisites

- Node.js 18.17 or later
- npm or pnpm

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   ```

3. **Configure API URL** (in `.env.local`)
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

### Development

Start the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

Build for production:

```bash
npm run build
```

Start production server:

```bash
npm start
```

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page (Dashboard)
│   └── globals.css         # Global styles
├── components/
│   ├── ui/                 # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   └── card.tsx
│   ├── layout/             # Layout components (Header, Sidebar)
│   └── shared/             # Shared/reusable components
├── lib/
│   ├── api/                # API client and endpoints
│   ├── hooks/              # Custom React hooks
│   ├── utils.ts            # Utility functions (cn helper)
│   └── validations/        # Zod validation schemas
├── types/                  # TypeScript type definitions
└── config/                 # Configuration files
    └── index.ts            # App configuration
```

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm start` | Start production server |
| `npm run lint` | Run ESLint |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |

## shadcn/ui Components

The following base components are pre-installed:

- **Button** - Clickable button with variants (default, secondary, destructive, outline, ghost, link)
- **Input** - Text input field
- **Card** - Card container with header, content, and footer

To add more components, visit [shadcn/ui](https://ui.shadcn.com/docs/components).

## Code Style

- ESLint for code linting
- Prettier for code formatting (with Tailwind CSS plugin)

Format code:
```bash
npx prettier --write .
```

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com)
- [Lucide Icons](https://lucide.dev)
