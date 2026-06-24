import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string) {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

export function getProficiencyColor(score: number) {
  if (score >= 90) return 'text-success';
  if (score >= 70) return 'text-primary';
  if (score >= 50) return 'text-accent';
  return 'text-secondary';
}
