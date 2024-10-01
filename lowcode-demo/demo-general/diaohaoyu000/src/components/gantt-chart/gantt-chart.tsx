import * as React from 'react';
import './index.scss';
import { createElement } from 'react';
export interface GanttChartProps {
    jobs?: string[];
    startTimes?: Date[];
    durations?: number[];
    equipmentIds?: string[];
    rowHeight?: number;
    columnWidth?: number;
    style?: React.CSSProperties;
}

const GanttChart: React.FC<GanttChartProps> = function GanttChart({
    jobs,
    startTimes,
    durations,
    equipmentIds,
    rowHeight = 40,
    columnWidth = 50,
    style = {},
    ...otherProps
}) {
    const uniqueEquipmentIds = Array.from(new Set(equipmentIds));

    // 根据任务动态生成颜色
    const generateColor = (task: string): string => {
        let hash = 0;
        for (let i = 0; i < task.length; i++) {
            hash = task.charCodeAt(i) + ((hash << 5) - hash);
        }
        const color = `#${((hash >> 24) & 0xFF).toString(16)}${((hash >> 16) & 0xFF).toString(16)}${((hash >> 8) & 0xFF).toString(16)}`.slice(0, 7);
        return color;
    };

    // 动态生成的任务颜色映射表
    const taskColors: { [key: string]: string } = {};
    jobs.forEach(job => {
        taskColors[job] = generateColor(job);
    });

    // 组件样式
    const _style = {
        ...style,
        display: 'flex',
        flexDirection: 'column',
        border: '1px solid #ddd',
        padding: '10px',
        backgroundColor: '#f5f5f5',
        position: 'relative',
    };

    // 计算任务的开始位置（基于天数差异）
    const getTaskPosition = (startTime: Date, earliestStartTime: Date): number => {
        return Math.floor((startTime.getTime() - earliestStartTime.getTime()) / (1000 * 60 * 60 * 24));
    };

    // 计算从起始日期开始的时间段
    const getDaysFromStart = (startDate: Date, endDate: Date): number => {
        return Math.ceil((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));
    };

    // 获取最早开始时间和最晚结束时间
    const earliestStartTime = new Date(Math.min(...startTimes.map(date => date.getTime())));
    const latestEndTime = new Date(Math.max(...startTimes.map((startTime, index) => startTime.getTime() + durations[index] * 24 * 60 * 60 * 1000)));

    // 计算总天数
    const totalDays = getDaysFromStart(earliestStartTime, latestEndTime) + Math.max(...durations);

    return (
        <div className="gantt-chart" style={_style} {...otherProps}>
            {/* 绘制设备名称及任务 */}
            <div style={{ display: 'flex', position: 'relative' }}>
                {/* 左侧纵轴，显示设备名称 */}
                <div style={{ minWidth: '100px', textAlign: 'right', fontWeight: 'bold', paddingRight: '10px' }}>
                    {uniqueEquipmentIds.map((equipmentId, eqIndex) => (
                        <div
                            key={eqIndex}
                            style={{
                                height: `${rowHeight}px`,
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'flex-end',
                            }}
                        >
                            {equipmentId}
                        </div>
                    ))}
                </div>

                {/* 任务部分 */}
                <div className="gantt-tasks" style={{ flexGrow: 1, position: 'relative' }}>
                    {uniqueEquipmentIds.map((equipmentId, eqIndex) => {
                        const equipmentTasks = jobs
                            .map((job, index) => ({
                                job,
                                startTime: startTimes[index],
                                duration: durations[index],
                                equipmentId: equipmentIds[index],
                            }))
                            .filter(task => task.equipmentId === equipmentId);

                        return (
                            <div
                                key={eqIndex}
                                className="gantt-task-row"
                                style={{
                                    height: `${rowHeight}px`,
                                    display: 'flex',
                                    position: 'relative',
                                    alignItems: 'center',
                                }}
                            >
                                {/* 背景竖线 */}
                                {Array.from({ length: totalDays }, (_, index) => (
                                    <div
                                        key={index}
                                        style={{
                                            position: 'absolute',
                                            left: `${index * columnWidth}px`,
                                            width: '1px',
                                            height: '100%',
                                            backgroundColor: '#ccc',
                                            boxSizing: 'border-box',
                                            zIndex: 0,
                                        }}
                                    />
                                ))}

                                {/* 任务条 */}
                                <div
                                    className="gantt-task-bars"
                                    style={{ display: 'flex', position: 'relative', height: `${rowHeight}px` }}
                                >
                                    {equipmentTasks.map((task, taskIndex) => {
                                        const taskStartIndex = getTaskPosition(task.startTime, earliestStartTime);
                                        const taskLength = task.duration * columnWidth;

                                        return (
                                            <div
                                                key={taskIndex}
                                                className="gantt-task-bar"
                                                style={{
                                                    position: 'absolute',
                                                    left: `${taskStartIndex * columnWidth}px`,
                                                    width: `${taskLength}px`,
                                                    backgroundColor: taskColors[task.job],
                                                    opacity: 0.8,
                                                    borderRadius: '5px',
                                                    height: '80%',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    justifyContent: 'center',
                                                    color: '#fff',
                                                    fontSize: '12px',
                                                }}
                                            >
                                                {task.job}
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* 在竖线下方显示时间 */}
            <div className="gantt-header" style={{ display: 'flex', marginTop: '10px', paddingLeft: '100px' }}>
                {Array.from({ length: totalDays }, (_, index) => {
                    const currentDate = new Date(earliestStartTime);
                    currentDate.setDate(currentDate.getDate() + index);
                    return (
                        <div
                            key={index}
                            className="gantt-header-day"
                            style={{
                                width: `${columnWidth}px`,
                                textAlign: 'center',
                                fontWeight: 'bold',
                            }}
                        >
                            {`${currentDate.getMonth() + 1}-${currentDate.getDate()}`}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default GanttChart;
