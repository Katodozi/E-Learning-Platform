import { cn } from '@/utils/cn';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'success' | 'secondary' | 'accent';
  className?: string;
}

const variants = {
  default: 'bg-primary/20 text-primary border-primary/30',
  success: 'bg-success/20 text-success border-success/30',
  secondary: 'bg-secondary/20 text-secondary border-secondary/30',
  accent: 'bg-accent/20 text-accent border-accent/30',
};

export function Badge({ children, variant = 'default', className }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium capitalize',
        variants[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}
