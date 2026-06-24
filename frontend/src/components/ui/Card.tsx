import { cn } from '@/utils/cn';

interface CardProps {
  className?: string;
  children: React.ReactNode;
  hover?: boolean;
}

export function Card({ className, children, hover }: CardProps) {
  return (
    <div
      className={cn(
        'glass rounded-xl p-6',
        hover && 'transition-all duration-300 hover:border-primary/30 hover:shadow-lg hover:shadow-primary/5',
        className,
      )}
    >
      {children}
    </div>
  );
}

export function CardHeader({ className, children }: { className?: string; children: React.ReactNode }) {
  return <div className={cn('mb-4', className)}>{children}</div>;
}

export function CardTitle({ className, children }: { className?: string; children: React.ReactNode }) {
  return <h3 className={cn('text-lg font-semibold text-text-primary', className)}>{children}</h3>;
}

export function CardDescription({ className, children }: { className?: string; children: React.ReactNode }) {
  return <p className={cn('text-sm text-text-secondary mt-1', className)}>{children}</p>;
}
