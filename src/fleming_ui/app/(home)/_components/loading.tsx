import { Loader2Icon } from "lucide-react";

const Loading = () => {
    return (<div className="flex items-center justify-center gap-2 p-4 mt-4" style={{
        flexGrow: 1,
    }}>
        <Loader2Icon className="animate-spin" />
    </div>);
}

export default Loading;
