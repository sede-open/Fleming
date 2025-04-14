import EmptyResult from "./empty-result";
import ResultCard from "./result-card";

interface ResultProps {
    results: Result[]
}

export interface Result {
    name: string;
    link: string;
    description: string;
    license: string;
    score: number;
}

const Results = ({ results }: ResultProps) => {
    return (<div className="flex flex-col gap-4 mt-4">
        {results.map((item) => (
            <ResultCard key={item.name} result={item} />
        ))}
        {results.length === 0 && (
            <EmptyResult />
        )}
    </div>);
}

export default Results;
