import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Trash2 } from 'lucide-react';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardDescription, CardTitle } from '@/components/ui/Card';
import { adminApi } from '@/services/api';

export function AdminPromptPage() {
  const queryClient = useQueryClient();
  const [form, setForm] = useState({ name: '', prompt_type: 'skill_content', template: '', is_active: true });

  const { data: prompts } = useQuery({
    queryKey: ['admin-prompts'],
    queryFn: () => adminApi.listPrompts().then((r) => r.data),
  });

  const createMutation = useMutation({
    mutationFn: () => adminApi.createPrompt(form),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-prompts'] });
      setForm({ name: '', prompt_type: 'skill_content', template: '', is_active: true });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => adminApi.deletePrompt(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-prompts'] }),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Manage Gemini Prompts</h1>

      <Card>
        <CardTitle className="text-base mb-3">Create Prompt Template</CardTitle>
        <div className="space-y-3">
          <div className="grid sm:grid-cols-2 gap-3">
            <Input placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            <select
              className="h-10 rounded-lg border border-border bg-surface/50 px-3 text-sm"
              value={form.prompt_type}
              onChange={(e) => setForm({ ...form, prompt_type: e.target.value })}
            >
              <option value="skill_content">Skill Content</option>
              <option value="quiz">Quiz</option>
            </select>
          </div>
          <textarea
            className="w-full h-40 rounded-lg border border-border bg-surface/50 px-3 py-2 text-sm resize-none"
            placeholder="Prompt template with {skill_name}, {topics}, etc."
            value={form.template}
            onChange={(e) => setForm({ ...form, template: e.target.value })}
          />
          <Button onClick={() => createMutation.mutate()}>Create Prompt</Button>
        </div>
      </Card>

      <div className="space-y-3">
        {prompts?.map((p) => (
          <Card key={p.id}>
            <div className="flex items-start justify-between gap-4">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <CardTitle className="text-base">{p.name}</CardTitle>
                  <Badge variant={p.is_active ? 'success' : 'secondary'}>{p.prompt_type}</Badge>
                </div>
                <CardDescription className="line-clamp-3 font-mono text-xs">{p.template}</CardDescription>
              </div>
              <Button variant="destructive" size="sm" onClick={() => deleteMutation.mutate(p.id)}>
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
