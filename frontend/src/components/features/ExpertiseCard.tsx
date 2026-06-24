import { motion } from 'framer-motion';
import {
  BarChart3,
  Brain,
  CheckCircle,
  Cloud,
  Code,
  Database,
  Layout,
  Network,
  Server,
  Shield,
  Smartphone,
} from 'lucide-react';
import { cn } from '@/utils/cn';
import type { Expertise } from '@/types';

const iconMap: Record<string, React.ElementType> = {
  layout: Layout,
  server: Server,
  database: Database,
  cloud: Cloud,
  'check-circle': CheckCircle,
  'bar-chart': BarChart3,
  pipeline: Database,
  brain: Brain,
  'cloud-lightning': Cloud,
  shield: Shield,
  smartphone: Smartphone,
  network: Network,
  code: Code,
};

interface ExpertiseCardProps {
  expertise: Expertise;
  onClick: () => void;
  index?: number;
}

export function ExpertiseCard({ expertise, onClick, index = 0 }: ExpertiseCardProps) {
  const Icon = iconMap[expertise.icon] || Code;

  return (
    <motion.button
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05, duration: 0.4 }}
      whileHover={{ y: -4, scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={cn(
        'glass rounded-xl p-6 text-left w-full',
        'transition-all duration-300 hover:border-primary/40',
        'hover:shadow-xl hover:shadow-primary/10 group',
      )}
    >
      <div className="flex items-start gap-4">
        <div className="rounded-lg bg-primary/10 p-3 group-hover:bg-primary/20 transition-colors">
          <Icon className="h-6 w-6 text-primary" />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-text-primary group-hover:text-primary transition-colors">
            {expertise.name}
          </h3>
          <p className="text-sm text-text-secondary mt-1 line-clamp-2">{expertise.description}</p>
        </div>
      </div>
    </motion.button>
  );
}
