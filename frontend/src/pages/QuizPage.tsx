import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate, useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, CheckCircle2, XCircle } from 'lucide-react';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Card, CardHeader, CardTitle } from '@/components/ui/Card';
import { quizApi } from '@/services/api';
import { cn, getProficiencyColor } from '@/utils/cn';
import type { QuizResult } from '@/types';

export function QuizPage() {
  const { skillId } = useParams<{ skillId: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [answers, setAnswers] = useState<number[]>([]);
  const [currentQ, setCurrentQ] = useState(0);
  const [result, setResult] = useState<QuizResult | null>(null);

  const { data: quiz, isLoading, error } = useQuery({
    queryKey: ['quiz', skillId],
    queryFn: () => quizApi.generate(Number(skillId)).then((r) => r.data),
    enabled: !!skillId,
    retry: false,
  });

  const submitMutation = useMutation({
    mutationFn: () => quizApi.submit(Number(skillId), answers),
    onSuccess: (res) => {
      setResult(res.data);
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['skill', skillId] });
    },
  });

  const selectAnswer = (optionIndex: number) => {
    const newAnswers = [...answers];
    newAnswers[currentQ] = optionIndex;
    setAnswers(newAnswers);
  };

  const handleNext = () => {
    if (currentQ < (quiz?.questions.length || 0) - 1) {
      setCurrentQ(currentQ + 1);
    }
  };

  const handleSubmit = () => {
    if (answers.length === 5 && answers.every((a) => a !== undefined)) {
      submitMutation.mutate();
    }
  };

  if (error) {
    return (
      <div className="max-w-2xl mx-auto text-center py-16">
        <p className="text-text-secondary mb-4">Complete all topics before taking the quiz.</p>
        <Button onClick={() => navigate(`/skill/${skillId}`)}>Back to Skill</Button>
      </div>
    );
  }

  if (result) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <Card className="text-center py-8">
          <div className={`text-5xl font-bold mb-2 ${getProficiencyColor(result.score)}`}>
            {result.score}%
          </div>
          <Badge variant="success" className="mb-4">{result.proficiency}</Badge>
          <p className="text-text-secondary">
            {result.correct_count} of {result.total_questions} correct
          </p>
        </Card>

        {result.results.map((r, i) => (
          <Card key={i}>
            <div className="flex items-start gap-3">
              {r.is_correct ? (
                <CheckCircle2 className="h-5 w-5 text-success shrink-0 mt-0.5" />
              ) : (
                <XCircle className="h-5 w-5 text-red-400 shrink-0 mt-0.5" />
              )}
              <div>
                <p className="font-medium mb-2">{r.question}</p>
                <p className="text-sm text-text-secondary">{r.explanation}</p>
              </div>
            </div>
          </Card>
        ))}

        <Button className="w-full" onClick={() => navigate('/dashboard')}>
          Back to Dashboard
        </Button>
      </div>
    );
  }

  const question = quiz?.questions[currentQ];

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <Button variant="ghost" size="sm" onClick={() => navigate(`/skill/${skillId}`)}>
        <ArrowLeft className="h-4 w-4 mr-2" /> Back to Skill
      </Button>

      {isLoading ? (
        <div className="glass rounded-xl h-64 animate-pulse" />
      ) : question ? (
        <>
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-bold">Skill Quiz</h1>
            <span className="text-sm text-text-secondary">
              Question {currentQ + 1} of {quiz?.questions.length}
            </span>
          </div>

          <div className="h-1.5 bg-surface rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-primary"
              initial={{ width: 0 }}
              animate={{ width: `${((currentQ + 1) / (quiz?.questions.length || 1)) * 100}%` }}
            />
          </div>

          <Card>
            <CardHeader>
              <CardTitle>{question.question}</CardTitle>
            </CardHeader>
            <div className="space-y-2">
              {question.options.map((option, i) => (
                <button
                  key={i}
                  onClick={() => selectAnswer(i)}
                  className={cn(
                    'w-full text-left p-3 rounded-lg border transition-all',
                    answers[currentQ] === i
                      ? 'border-primary bg-primary/10 text-text-primary'
                      : 'border-border hover:border-primary/30 text-text-secondary',
                  )}
                >
                  <span className="font-medium mr-2">{String.fromCharCode(65 + i)}.</span>
                  {option}
                </button>
              ))}
            </div>
          </Card>

          <div className="flex gap-3">
            {currentQ < (quiz?.questions.length || 0) - 1 ? (
              <Button
                className="flex-1"
                disabled={answers[currentQ] === undefined}
                onClick={handleNext}
              >
                Next Question
              </Button>
            ) : (
              <Button
                className="flex-1"
                disabled={answers.length < 5 || answers.some((a) => a === undefined) || submitMutation.isPending}
                onClick={handleSubmit}
              >
                {submitMutation.isPending ? 'Submitting...' : 'Submit Quiz'}
              </Button>
            )}
          </div>
        </>
      ) : null}
    </div>
  );
}
