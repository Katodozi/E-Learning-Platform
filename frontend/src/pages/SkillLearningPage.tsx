import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, CheckCircle2, Circle, Sparkles } from 'lucide-react';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { skillApi } from '@/services/api';

export function SkillLearningPage() {
  const { skillId } = useParams<{ skillId: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: skill, isLoading } = useQuery({
    queryKey: ['skill', skillId],
    queryFn: () => skillApi.getSkill(Number(skillId)).then((r) => r.data),
    enabled: !!skillId,
  });

  const completeMutation = useMutation({
    mutationFn: (topicId: number) => skillApi.completeTopic(topicId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['skill', skillId] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
  });

  const allTopicsCompleted = skill?.topics.every((t) => t.completed);

  const sections = skill
    ? [
        { title: 'Overview', content: skill.overview },
        { title: 'Core Concepts', content: skill.core_concepts },
        { title: 'Basic Explanation', content: skill.basic_explanation },
        { title: 'Real World Example', content: skill.real_world_example },
        { title: 'Summary', content: skill.summary },
      ]
    : [];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <Button variant="ghost" size="sm" onClick={() => navigate('/dashboard')}>
        <ArrowLeft className="h-4 w-4 mr-2" /> Back to Dashboard
      </Button>

      {isLoading ? (
        <div className="glass rounded-xl h-96 animate-pulse" />
      ) : skill ? (
        <>
          <div className="flex items-start justify-between gap-4 flex-wrap">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <h1 className="text-2xl md:text-3xl font-bold">{skill.skill_name}</h1>
                {skill.cached && (
                  <Badge variant="accent">
                    <Sparkles className="h-3 w-3 mr-1" /> Cached
                  </Badge>
                )}
              </div>
              <p className="text-text-secondary">AI-generated beginner-friendly content</p>
            </div>
            {allTopicsCompleted && (
              <Link to={`/quiz/${skill.skill_id}`}>
                <Button variant="accent">Take Quiz</Button>
              </Link>
            )}
          </div>

          {sections.map((section, i) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle>{section.title}</CardTitle>
                </CardHeader>
                <div className="text-text-secondary whitespace-pre-wrap leading-relaxed">
                  {section.content}
                </div>
              </Card>
            </motion.div>
          ))}

          <Card>
            <CardHeader>
              <CardTitle>Topics</CardTitle>
              <CardDescription>Mark each topic as complete when you've understood it</CardDescription>
            </CardHeader>
            <div className="space-y-2">
              {skill.topics.map((topic) => (
                <div
                  key={topic.id}
                  className="flex items-center justify-between gap-4 p-3 rounded-lg bg-surface/50"
                >
                  <div className="flex items-center gap-3">
                    {topic.completed ? (
                      <CheckCircle2 className="h-5 w-5 text-success shrink-0" />
                    ) : (
                      <Circle className="h-5 w-5 text-text-secondary shrink-0" />
                    )}
                    <div>
                      <p className="font-medium">{topic.name}</p>
                      <p className="text-xs text-text-secondary">{topic.description}</p>
                    </div>
                  </div>
                  {!topic.completed && (
                    <Button
                      size="sm"
                      variant="outline"
                      disabled={completeMutation.isPending}
                      onClick={() => completeMutation.mutate(topic.id)}
                    >
                      Complete
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </Card>
        </>
      ) : (
        <p className="text-text-secondary">Skill not found.</p>
      )}
    </div>
  );
}
