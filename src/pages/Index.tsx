import { useState, useEffect } from "react";
import axios from "axios";
import { Eye, Brain, Factory, TrendingUp, Database, Shield, Bot, Zap } from "lucide-react";
import { NeuralBackground } from "@/components/NeuralBackground";
import { Header } from "@/components/Header";
import { OrganismCore } from "@/components/OrganismCore";
import { OrganEngine } from "@/components/OrganEngine";
import { AgentCard } from "@/components/AgentCard";
import { OrganismCard, OrganismCardHeader, OrganismCardTitle, OrganismCardContent } from "@/components/ui/organism-card";
import { MetricDisplay } from "@/components/ui/metric-display";
import { ActivityLog } from "@/components/ui/activity-log";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";

interface OrganismState {
  generation: number;
  problemsScanned: number;
  ideasGenerated: number;
  productsBuilt: number;
  revenue: number;
  agentsActive: number;
  agentsTerminated: number;
  status: 'online' | 'processing' | 'idle' | 'error';
}

interface LogEntry {
  timestamp: string;
  type: 'info' | 'success' | 'warning' | 'error';
  message: string;
}

interface Agent {
  id: string;
  name: string;
  type: 'research' | 'builder' | 'growth' | 'support';
  status: 'idle' | 'working' | 'terminated';
  tasksCompleted: number;
  uptime: string;
  efficiency: number;
}

interface Idea {
  theme: string;
  score: number;
  summary: string;
}

export default function Index() {
  const [state, setState] = useState<OrganismState>({
    generation: 1,
    problemsScanned: 0,
    ideasGenerated: 0,
    productsBuilt: 0,
    revenue: 0,
    agentsActive: 0,
    agentsTerminated: 0,
    status: 'online',
  });
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleScrape = async () => {
    setIsLoading(true);
    setLogs(prev => [...prev, { timestamp: new Date().toISOString(), type: 'info', message: 'Scraping for problems...' }]);
    try {
      await axios.post('/api/sense/scrape?subreddit=startupideas');
      const ideasResponse = await axios.get('/api/decision/ideas');
      setIdeas(ideasResponse.data);
      setState(prevState => ({
        ...prevState,
        ideasGenerated: ideasResponse.data.length,
        problemsScanned: prevState.problemsScanned + 100 // placeholder
      }));
      setLogs(prev => [...prev, { timestamp: new Date().toISOString(), type: 'success', message: `Generated ${ideasResponse.data.length} new ideas.` }]);
    } catch (error) {
      console.error("Error scraping data:", error);
      setLogs(prev => [...prev, { timestamp: new Date().toISOString(), type: 'error', message: 'Failed to scrape data.' }]);
    }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-background text-foreground relative overflow-hidden">
      <NeuralBackground />
      
      <div className="relative z-10">
        <Header 
          organismName="ORGANISM-ALPHA" 
          generation={state.generation} 
          status={state.status}
        />

        <main className="container mx-auto px-4 py-8">
          {/* ... existing JSX ... */}

          <Button onClick={handleScrape} disabled={isLoading}>
            {isLoading ? "Scanning..." : "Scan for Problems"}
          </Button>

          {/* Display Ideas */}
          <section className="mt-8">
            <h3 className="text-lg font-semibold mb-4">Generated Ideas</h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {ideas.map((idea, index) => (
                <OrganismCard key={index} variant="default">
                  <OrganismCardHeader>
                    <OrganismCardTitle>{idea.theme}</OrganismCardTitle>
                  </OrganismCardHeader>
                  <OrganismCardContent>
                    <p className="text-sm text-muted-foreground">{idea.summary}</p>
                    <p className="text-right text-primary font-bold mt-4">{idea.score.toFixed(2)}</p>
                  </OrganismCardContent>
                </OrganismCard>
              ))}
            </div>
          </section>

          {/* ... rest of the JSX ... */}
        </main>
      </div>
    </div>
  );
}
