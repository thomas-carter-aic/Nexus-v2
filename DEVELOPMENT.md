# Development Guide

## Quick Start

1. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

2. **Start the backend** (in another terminal):
   ```bash
   cd ../ultimate-paas-base
   # Follow backend setup instructions
   ```

3. **Start all microfrontends**:
   ```bash
   npm run dev
   ```

## Development Workflow

### Adding a New Component to UI Package

```bash
# Navigate to UI package
cd packages/ui/src

# Create new component file
touch my-component.tsx

# Export from index
echo 'export * from "./src/my-component";' >> ../index.tsx
```

### Creating a New Microfrontend

1. **Create the app directory**:
   ```bash
   mkdir apps/my-new-app
   ```

2. **Copy package.json from existing app and modify**:
   ```bash
   cp apps/dashboard/package.json apps/my-new-app/
   # Edit the name and port in package.json
   ```

3. **Set up the basic structure**:
   ```bash
   mkdir -p apps/my-new-app/{app,components,lib}
   ```

### Working with Shared Packages

- **Types**: Add new types to `packages/types/index.ts`
- **Auth**: Extend auth functionality in `packages/auth/src/`
- **API Client**: Add new API calls to `packages/api-client/src/`

### Environment Variables

Each app has its own `.env.local` file. Common variables:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GRAPHQL_URL=http://localhost:8000/graphql
NEXTAUTH_URL=http://localhost:3000  # Change port for each app
NEXTAUTH_SECRET=your-secret-key
```

### Testing

```bash
# Run tests for all packages
npm run test

# Run tests for specific package
npm run test --filter=@ultimate-paas/ui

# Type checking
npm run type-check
```

### Building

```bash
# Build all packages and apps
npm run build

# Build specific app
npm run build --filter=@ultimate-paas/dashboard
```

## Architecture Decisions

### Why Turborepo?

- **Incremental builds**: Only rebuilds what changed
- **Parallel execution**: Runs tasks across packages simultaneously
- **Dependency graph**: Understands package relationships
- **Caching**: Speeds up repeated builds

### Why Microfrontends?

- **Independent deployment**: Each app can be deployed separately
- **Team autonomy**: Different teams can work on different apps
- **Technology flexibility**: Each app can use different versions/tools
- **Scalability**: Scale development teams and applications independently

### State Management Strategy

- **Zustand**: For client-side global state (auth, user preferences)
- **TanStack Query**: For server state management and caching
- **React State**: For component-local state

### Styling Approach

- **Tailwind CSS**: Utility-first CSS framework
- **CSS Variables**: For theming and customization
- **Component variants**: Using class-variance-authority for component variants

## Common Issues

### Port Conflicts

Each microfrontend runs on a different port:
- Dashboard: 3000
- App Management: 3001
- Deployment: 3002
- AI Analytics: 3003
- Plugin Management: 3004
- Security: 3005
- Monitoring: 3006

### Package Resolution Issues

If you encounter package resolution issues:

```bash
# Clean everything
npm run clean

# Remove node_modules
rm -rf node_modules apps/*/node_modules packages/*/node_modules

# Reinstall
npm install
```

### TypeScript Errors

```bash
# Check types across all packages
npm run type-check

# Check specific package
npm run type-check --filter=@ultimate-paas/dashboard
```

## Best Practices

### Component Development

1. **Start with the UI package**: Create reusable components in `packages/ui`
2. **Use TypeScript**: Always type your components and props
3. **Follow naming conventions**: Use PascalCase for components, camelCase for functions
4. **Document with JSDoc**: Add comments for complex components

### API Integration

1. **Use the API client**: Don't create axios instances directly
2. **Handle errors gracefully**: Always handle API errors
3. **Use React Query**: For caching and synchronization
4. **Type your responses**: Use types from `@ultimate-paas/types`

### Authentication

1. **Check permissions**: Use `hasPermission()` for feature access
2. **Handle unauthenticated states**: Always provide fallbacks
3. **Secure routes**: Use auth guards for protected pages
4. **Token management**: Let the auth package handle tokens

## Deployment

### Development

```bash
npm run build
npm run start
```

### Production

Each microfrontend can be deployed independently to platforms like:

- **Vercel**: Automatic deployments from Git
- **Netlify**: Static site hosting
- **AWS S3 + CloudFront**: Custom deployment
- **Docker**: Containerized deployment

### Environment-Specific Builds

```bash
# Development build
NODE_ENV=development npm run build

# Production build
NODE_ENV=production npm run build
```
