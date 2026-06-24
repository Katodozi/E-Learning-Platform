import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Plus, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardTitle } from '@/components/ui/Card';
import { adminApi } from '@/services/api';

export function AdminExpertisePage() {
  const queryClient = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ name: '', slug: '', description: '', icon: 'code' });

  const { data: expertise } = useQuery({
    queryKey: ['admin-expertise'],
    queryFn: () => adminApi.listExpertise().then((r) => r.data),
  });

  const createMutation = useMutation({
    mutationFn: () => adminApi.createExpertise(form),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-expertise'] });
      setShowForm(false);
      setForm({ name: '', slug: '', description: '', icon: 'code' });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => adminApi.deleteExpertise(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-expertise'] }),
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Manage Expertise</h1>
        <Button size="sm" onClick={() => setShowForm(!showForm)}>
          <Plus className="h-4 w-4 mr-1" /> Add
        </Button>
      </div>

      {showForm && (
        <Card>
          <div className="grid sm:grid-cols-2 gap-3">
            <Input placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            <Input placeholder="Slug" value={form.slug} onChange={(e) => setForm({ ...form, slug: e.target.value })} />
            <Input placeholder="Description" className="sm:col-span-2" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            <Button onClick={() => createMutation.mutate()} disabled={createMutation.isPending}>Create</Button>
          </div>
        </Card>
      )}

      <div className="space-y-3">
        {expertise?.map((exp) => (
          <Card key={exp.id}>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-base">{exp.name}</CardTitle>
                <p className="text-sm text-text-secondary">{exp.slug}</p>
              </div>
              <Button variant="destructive" size="sm" onClick={() => deleteMutation.mutate(exp.id)}>
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
