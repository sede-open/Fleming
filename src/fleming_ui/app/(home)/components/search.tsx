import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { FilterIcon, SearchIcon } from "lucide-react";
import { useState } from "react";

const Search = ({
    setShowFilters,
    setSearchQuery
}: {
    setShowFilters: React.Dispatch<React.SetStateAction<boolean>>;
    setSearchQuery: React.Dispatch<React.SetStateAction<string>>;
}) => {
    const [inputValue, setInputValue] = useState("");
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setInputValue(event.target.value);
    };
    const handleSearch = () => {
        setSearchQuery(inputValue);
    }
    return (
        <div className="flex items-center justify-center gap-2 h-12 mt-4">
            <Input placeholder="Enter Prompt to Search" className="h-full"
                onChange={
                    handleInputChange
                }
                value={inputValue}
                onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                        handleSearch();
                    }
                }}
            />
            <Button className="h-full" onClick={handleSearch}>
                <SearchIcon className="w-4 h-4" />
                Search
            </Button>
            <Button variant="outline" className="h-full" onClick={() => setShowFilters((prev) => !prev)}>
                <FilterIcon className="w-4 h-4" />
                Filter
            </Button>
        </div>
    );
}

export default Search;
