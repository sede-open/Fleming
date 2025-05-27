import { MessageSquareWarning } from "lucide-react";

const Error = () => {
    return (<div
        className="flex flex-col items-center justify-center gap-2 p-4 text-center bg-red-100 border border-red-300 rounded-md mt-4">
        <MessageSquareWarning className="w-10 h-10 text-red-700" />
        <h2 className="text-lg font-semibold text-red-700">Something went wrong</h2>
        <p className="text-sm text-red-600">We couldn&apos;t fetch the data you requested.</p>
        <p className="text-sm text-red-600">Please try again later.</p>
    </div>);
}

export default Error;
