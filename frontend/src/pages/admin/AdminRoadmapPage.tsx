import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Trash2 } from 'lucide-react';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardTitle } from '@/components/ui/Card';
import { adminApi } from '@/services/api';

export function AdminRoadmapPage() {
  const queryClient = useQueryClient();
  const [expertiseFilter, setExpertiseFilter] = useState<number | undefined>();
  const [form, setForm] = useState({
    expertise_id: 0,
    title: '',
    level: 'beginner',
    description: '',
    estimated_duration: '4-6 weeks',
  });

  const { data: expertise } = useQuery({
    queryKey: ['admin-expertise'],
    queryFn: () => adminApi.listExpertise().then((r) => r.data),
  });

  const { data: roadmaps } = useQuery({
    queryKey: ['admin-roadmaps', expertiseFilter],
    queryFn: () => adminApi.listRoadmaps(expertiseFilter).then((r) => r.data),
  });

  const createMutation = useMutation({
    mutationFn: () => adminApi.createRoadmap(form),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-roadmaps'] }),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => adminApi.deleteRoadmap(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-roadmaps'] }),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Manage Roadmaps</h1>

      <div className="flex gap-2 flex-wrap">
        <Button size="sm" variant={!expertiseFilter ? 'default' : 'outline'} onClick={() => setExpertiseFilter(undefined)}>
          All
        </Button>
        {expertise?.map((e) => (
          <Button key={e.id} size="sm" variant={expertiseFilter === e.id ? 'default' : 'outline'} onClick={() => setExpertiseFilter(e.id)}>
            {e.name}
          </Button>
        ))}
      </div>

      <Card>
        <CardTitle className="text-base mb-3">Create Roadmap</CardTitle>
        <div className="grid sm:grid-cols-2 gap-3">
          <select
            className="h-10 rounded-lg border border-border bg-surface/50 px-3 text-sm"
            value={form.expertise_id}
            onChange={(e) => setForm({ ...form, expertise_id: Number(e.target.value) })}
          >
            <option value={0}>Select expertise</option>
            {expertise?.map((e) => (
              <option key={e.id} value={e.id}>{e.name}</option>
            ))}
          </select>
          <Input placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
          <select
            className="h-10 rounded-lg border border-border bg-surface/50 px-3 text-sm"
            value={form.level}
            onChange={(e) => setForm({ ...form, level: e.target.value })}
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
          <Input placeholder="Duration" value={form.estimated_duration} onChange={(e) => setForm({ ...form, estimated_duration: e.target.value })} />
          <Input placeholder="Description" className="sm:col-span-2" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
          <Button onClick={() => createMutation.mutate()} disabled={!form.expertise_id}>Create</Button>
        </div>
      </Card>

      <div className="space-y-3">
        {roadmaps?.map((r) => (
          <Card key={r.id}>
            <div className="flex items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <CardTitle className="text-base">{r.title}</CardTitle>
                  <Badge>{r.level}</Badge>
                </div>
                <p className="text-sm text-text-secondary">{r.estimated_duration} · {r.skill_count} skills</p>
              </div>
              <Button variant="destructive" size="sm" onClick={() => deleteMutation.mutate(r.id)}>
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
