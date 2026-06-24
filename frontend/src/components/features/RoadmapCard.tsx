import { motion } from 'framer-motion';
import { Clock, Layers } from 'lucide-react';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import type { RoadmapSummary } from '@/types';

interface RoadmapCardProps {
  roadmap: RoadmapSummary;
  onPreview: () => void;
  onStart: () => void;
  index?: number;
  highlighted?: boolean;
}

const levelColors: Record<string, 'default' | 'success' | 'secondary' | 'accent'> = {
  beginner: 'success',
  intermediate: 'default',
  advanced: 'secondary',
};

export function RoadmapCard({ roadmap, onPreview, onStart, index = 0, highlighted }: RoadmapCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
    >
      <Card
        hover
        className={highlighted ? 'border-primary/50 ring-1 ring-primary/20' : ''}
      >
        <CardHeader>
          <div className="flex items-center justify-between gap-2">
            <Badge variant={levelColors[roadmap.level] || 'default'}>{roadmap.level}</Badge>
            <div className="flex items-center gap-1 text-xs text-text-secondary">
              <Clock className="h-3.5 w-3.5" />
              {roadmap.estimated_duration}
            </div>
          </div>
          <CardTitle>{roadmap.title}</CardTitle>
          <CardDescription>{roadmap.description}</CardDescription>
        </CardHeader>

        <div className="flex items-center gap-2 text-sm text-text-secondary mb-6">
          <Layers className="h-4 w-4" />
          {roadmap.skill_count} skills included
        </div>

        <div className="flex gap-2">
          <Button variant="outline" size="sm" className="flex-1" onClick={onPreview}>
            Preview
          </Button>
          <Button size="sm" className="flex-1" onClick={onStart}>
            Start Learning
          </Button>
        </div>
      </Card>
    </motion.div>
  );
}
