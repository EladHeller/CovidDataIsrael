const {
    MenuItem, Select, InputLabel, FormHelperText, FormControlLabel, Switch, Checkbox, Typography, Slider
} = MaterialUI;

const HistorySlider = ({onHistory}) => {
    const [dates, setDates] = React.useState([]);
    const [pos, setPos] = React.useState(100);
    React.useEffect(() => {
        (async () => {
            const data = await fetchFile('out/history/dates.json');
            setDates(data ? JSON.parse(data) : []);
        })();
    }, []);
    return <Slider
        disabled={!dates.length}
        value={pos}
        onChange={(e, v) => {
            setPos(v);
            onHistory(v === 100 ? false : dates[Math.round(val / 100 * (dates.length - 1))]);
        }}
        step={dates.length ? 100 / dates.length : undefined}
        valueLabelDisplay="auto"
        valueLabelFormat={val => {
            const d = new Date(dates[Math.round(val / 100 * (dates.length - 1))])
            return d.getDate() + '.' + (d.getMonth() + 1)
        }}
    />
}

// const HistoryLoader = ({name, onHistory}) => {
//     return
// }