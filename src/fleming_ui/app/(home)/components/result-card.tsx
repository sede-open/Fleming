import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Result } from "./result";
import { Badge } from "@/components/ui/badge";
import { Link } from "lucide-react";
import { useState } from "react";

const ResultCard = ({ result }: { result: Result }) => {
    const scorePercent = result.score * 100;
    const [isExpanded, setIsExpanded] = useState(false);
    const [hasEllipsis, setHasEllipsis] = useState(false);
    const getBadgeColor = (score: number) => {
        if (score > 60) return "bg-green-100 text-green-800 hover:bg-green-200";
        if (score >= 40) return "bg-orange-100 text-orange-800 hover:bg-orange-200";
        return "bg-red-100 text-red-800 hover:bg-red-200";
    };
    return (
        <Card className="h-full hover:shadow-md transition-shadow duration-300 gap-2">
            <CardHeader>
                <div className="flex justify-between items-start">
                    <h2 className="text-xl font-semibold">{result.name}</h2>
                    <Badge className={getBadgeColor(scorePercent)}>
                        Score: {scorePercent.toFixed(1)}%
                    </Badge>
                </div>
            </CardHeader>
            <CardContent>
                <div className="flex flex-col space-y-2">
                    <div>
                        <p className={`text-sm text-gray-500 ${!isExpanded ? 'line-clamp-2' : ''}`} ref={(el) => {
                            if (el && !isExpanded) {
                                setHasEllipsis(el.scrollHeight > el.clientHeight);
                            }
                        }}>
                            {result.description}
                        </p>
                        {!isExpanded && hasEllipsis && (
                            <button
                                onClick={() => setIsExpanded(true)}
                                className="text-xs text-blue-600 hover:text-blue-800 "
                            >
                                Show more
                            </button>
                        )}
                        {isExpanded && (
                            <button
                                onClick={() => setIsExpanded(false)}
                                className="text-xs text-blue-600 hover:text-blue-800 ml-1"
                            >
                                Show less
                            </button>
                        )}
                    </div>
                    <a
                        href={result.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 transition-colors duration-200 truncate flex items-center gap-1 mt-2"
                    >
                        <Link className="w-3 h-3" />
                        {result.link}
                    </a>
                    {result.license && (
                        <div className="flex items-center gap-2">
                            <span className="text-xs font-medium text-gray-600">License:</span>
                            <Badge
                                variant="outline"
                                className="text-xs px-2 py-0.5 bg-blue-50 text-blue-700 border border-blue-200"
                            >
                                {result.license}
                            </Badge>
                        </div>
                    )}
                </div>
            </CardContent>
        </Card >
    )
}

export default ResultCard;
