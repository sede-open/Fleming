export function TransformData(data: {
    predictions: string[];
}) {
    const { predictions } = data;
    const transformedData = predictions.map((prediction) => {
        const [content, score] = prediction;
        const parsedContent = parseContent(content);
        return {
            ...parsedContent,
            score: parseFloat(score),
        };
    });
    return transformedData;
}
function parseContent(content: string) {
    try {
        const { Name, Link, Summary, filter } = JSON.parse(content);
        const { LicenceFileContent, Archived } = filter;
        const result = {
            name: Name,
            link: Link,
            license: LicenceFileContent,
            archived: Archived,
            description: Summary
        };
        return result;
    } catch (error) {
        console.log("Error", error)
        return null;
    }

}
