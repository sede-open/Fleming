const Greetings = () => {
    return (
        <div className="flex flex-col justify-center gap-2">
            <h3 className="text-3xl">
                Welcome to the
            </h3>
            <h1 className="text-4xl font-bold">
                Project Fleming Demo Front End
            </h1>
            <p className="text-lg text-muted-foreground mt-2">
                This is a generic UI for Project Fleming, where you can search for GitHub repositories using natural language queries.
                Powered by LLM technology, it interprets your search and displays comprehensive repository details.
            </p>
        </div>
    );
}

export default Greetings;
