import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";
import axios from "axios";
import { toast } from "sonner";
import IdeasDisplay from "@/components/IdeasDisplay";

const Index = () => {
  const [url, setUrl] = useState("https://www.reddit.com/r/SaaS/top/?t=month");
  const [source, setSource] = useState("reddit");
  const [loading, setLoading] = useState(false);

  const handleScrape = async () => {
    setLoading(true);
    try {
      await axios.post("/api/scrape", { url, source });
      toast.success("Scraping started successfully!");
    } catch (error) {
      console.error("Error starting scrape:", error);
      toast.error("Failed to start scraping.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Autonomous SaaS Organism</h1>
      <Card className="mb-4">
        <CardHeader>
          <CardTitle>Sense Engine</CardTitle>
          <CardDescription>
            Scrape a website to find new problems.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="url">URL to Scrape</Label>
            <Input
              id="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
          </div>
          <div>
            <Label htmlFor="source">Source</Label>
            <Input
              id="source"
              value={source}
              onChange={(e) => setSource(e.target.value)}
            />
          </div>
        </CardContent>
        <CardFooter>
          <Button onClick={handleScrape} disabled={loading}>
            {loading ? "Scraping..." : "Scrape"}
          </Button>
        </CardFooter>
      </Card>
      <IdeasDisplay />
    </div>
  );
};

export default Index;
