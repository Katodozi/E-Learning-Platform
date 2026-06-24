import { forwardRef, type ButtonHTMLAttributes } from 'react';
import { cn } from '@/utils/cn';

const variants = {
  default: 'bg-primary hover:bg-primary/90 text-white',
  secondary: 'bg-secondary hover:bg-secondary/90 text-white',
  outline: 'border border-border bg-transparent hover:bg-surface text-text-primary',
  ghost: 'hover:bg-surface text-text-secondary hover:text-text-primary',
  accent: 'bg-accent hover:bg-accent/90 text-white',
  destructive: 'bg-red-600 hover:bg-red-700 text-white',
};

const sizes = {
  sm: 'h-8 px-3 text-sm',
  md: 'h-10 px-4',
  lg: 'h-12 px-6 text-lg',
};

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: keyof typeof variants;
  size?: keyof typeof sizes;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'md', ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        'inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary',
        'disabled:pointer-events-none disabled:opacity-50',
        variants[variant],
        sizes[size],
        className,
      )}
      {...props}
    />
  ),
);
Button.displayName = 'Button';
