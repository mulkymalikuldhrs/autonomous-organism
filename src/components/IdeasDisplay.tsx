import { useEffect, useState } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";

interface Idea {
  text: string;
  cluster: number;
  sentiment: {
    neg: number;
    neu: number;
    pos: number;
    compound: number;
  };
}

const IdeasDisplay = () => {
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchIdeas = async () => {
    setLoading(true);
    try {
      const response = await axios.get("/api/ideas");
      setIdeas(response.data.ideas);
    } catch (error) {
      console.error("Error fetching ideas:", error);
      toast.error("Failed to fetch ideas.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIdeas();
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Problem Ideas</CardTitle>
      </CardHeader>
      <CardContent>
        <Button onClick={fetchIdeas} disabled={loading}>
          {loading ? "Refreshing..." : "Refresh Ideas"}
        </Button>
        <div className="mt-4 space-y-4">
          {ideas.map((idea, index) => (
            <Card key={index} className="p-4">
              <p>{idea.text}</p>
              <div className="flex justify-between text-sm text-gray-500 mt-2">
                <span>Cluster: {idea.cluster}</span>
                <span>Sentiment (Compound): {idea.sentiment.compound}</span>
              </div>
            </Card>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default IdeasDisplay;
