
/**
 * Transforms an array of activity objects into x-y coordinate objects.
 * @param {Array<Object>} activities - array of activity objects.
 * @param {string} yAxis - Key name to use for y-axis values.
 * @param {string} xAxis - Key name to use for x-axis values.
 * @returns {Array<Object>} - array of objects with x and y properties.
 */
export default function getXYData(activities, yAxis, xAxis) {
    const dataToPlot = []
    for (const activity of activities) {
        const activityXY = {x: activity[xAxis], y: activity[yAxis]}
        dataToPlot.push(activityXY)
    }
    return dataToPlot
}
