import { MultiSelect } from "@/components/ui/multi-select";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { useState } from "react";

// const frameworksList = [
//     { value: "react", label: "React" },
//     { value: "angular", label: "Angular" },
//     { value: "vue", label: "Vue" },
//     { value: "svelte", label: "Svelte" },
//     { value: "ember", label: "Ember" },
// ];

const Filters = ({ setSort }: {
    setSort: (sort: string) => void;
}) => {
    const [selectedFrameworks, setSelectedFrameworks] = useState<string[]>([]);
    return (<div>
        <div className="flex items-center justify-between gap-4 mt-4">
            {/* <MultiSelect
                options={frameworksList}
                onValueChange={setSelectedFrameworks}
                defaultValue={selectedFrameworks}
                placeholder="Select frameworks"
                variant="inverted"
                maxCount={3}
                className="w-[360px] h-full"
            /> */}

            <Select
                onValueChange={(value) => {
                    setSort(value);
                }}
                defaultValue="score"
            >
                <SelectTrigger className="w-[180px] h-full">
                    <SelectValue placeholder="Sort by" />
                </SelectTrigger>
                <SelectContent >
                    <SelectItem value="score">Score</SelectItem>
                    <SelectItem value="alpha">Alphabetical</SelectItem>
                </SelectContent>
            </Select>
        </div>
    </div >);
}

export default Filters;
