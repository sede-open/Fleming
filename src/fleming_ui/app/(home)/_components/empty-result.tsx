import { Search } from "lucide-react";

const EmptyResult = () => {
    return (
        <div className="flex flex-col items-center justify-center gap-4 p-8">
            <div className="p-3 bg-blue-50 rounded-full">
                <Search className="w-10 h-10 text-blue-600" />
            </div>
            <h2 className="text-xl font-medium text-gray-800">
                Ready to search repositories
            </h2>
            <p className="text-gray-600 text-center max-w-md">
                Enter keywords to find repositories by name, description, or filter by programming language.
            </p>
        </div>
    );
}

export default EmptyResult;
