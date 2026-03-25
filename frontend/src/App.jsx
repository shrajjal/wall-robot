import { useState } from "react";
import axios from "axios";

export default function App() {
  const [width, setWidth] = useState(10);
  const [height, setHeight] = useState(8);
  const [obstacles, setObstacles] = useState([]);
  const [animatedPath, setAnimatedPath] = useState([]);
  const [speed, setSpeed] = useState(80);
  const [isDrawing, setIsDrawing] = useState(false);
  const [isRunning, setIsRunning] = useState(false);

  // ---------------------------
  // 🔹 Toggle obstacle
  // ---------------------------
  const toggleObstacle = (x, y) => {
    const exists = obstacles.some(o => o.x === x && o.y === y);

    if (exists) {
      setObstacles(obstacles.filter(o => !(o.x === x && o.y === y)));
    } else {
      setObstacles([...obstacles, { x, y, width: 1, height: 1 }]);
    }
  };

  // ---------------------------
  // 🔹 Sleep (animation delay)
  // ---------------------------
  const sleep = (ms) => new Promise(res => setTimeout(res, ms));

  // ---------------------------
  // 🔹 Generate path + animate
  // ---------------------------
  const generatePath = async () => {
    if (isRunning) return;

    setIsRunning(true);
    setAnimatedPath([]);

    try {
      const res = await axios.post("http://127.0.0.1:8000/trajectory", {
        width,
        height,
        obstacles
      });

      const fullPath = res.data.path;

      for (let i = 0; i < fullPath.length; i++) {
        setAnimatedPath(prev => [...prev, fullPath[i]]);
        await sleep(speed);
      }

    } catch (err) {
      console.error(err);
    }

    setIsRunning(false);
  };

  // ---------------------------
  // 🔹 Metrics
  // ---------------------------
  const totalSteps = animatedPath.length;
  const uniqueCells = new Set(animatedPath.map(p => `${p[0]}-${p[1]}`)).size;
  const revisits = totalSteps - uniqueCells;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-gray-300 flex">

      {/* ===========================
          🔹 CONTROL PANEL
      =========================== */}
      <div className="w-64 bg-white shadow-lg p-4">

        <h2 className="text-xl font-bold mb-4">Controls</h2>

        {/* Grid size */}
        <div className="mb-4 flex gap-2">
          <input
            type="number"
            value={width}
            onChange={(e) => setWidth(+e.target.value)}
            className="border p-1 w-16 rounded"
          />
          <input
            type="number"
            value={height}
            onChange={(e) => setHeight(+e.target.value)}
            className="border p-1 w-16 rounded"
          />
        </div>

        {/* Speed */}
        <div className="mb-4">
          <label className="text-sm font-semibold">Speed</label>
          <input
            type="range"
            min="20"
            max="200"
            value={speed}
            onChange={(e) => setSpeed(+e.target.value)}
            className="w-full"
          />
          <div className="text-xs text-gray-500">{speed} ms</div>
        </div>

        {/* Buttons */}
        <button
          onClick={generatePath}
          className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-2 rounded w-full mb-2"
        >
          Generate Path
        </button>

        <button
          onClick={() => setAnimatedPath([])}
          className="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-2 rounded w-full mb-2"
        >
          Reset Path
        </button>

        <button
          onClick={() => {
            setObstacles([]);
            setAnimatedPath([]);
          }}
          className="bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded w-full"
        >
          Clear All
        </button>

        {/* ===========================
            🔹 METRICS PANEL
        =========================== */}
        <div className="mt-6 text-sm bg-gray-50 p-3 rounded shadow-inner">
          <p >📍 Total Steps: <b>{totalSteps}</b></p>
          <p>✅ Unique Cells: <b>{uniqueCells}</b></p>
          <p>🔁 Revisits: <b>{revisits}</b></p>
        </div>
      </div>

      {/* ===========================
          🔹 GRID
      =========================== */}
      <div className="flex-1 flex justify-center items-center">

        <div
          className="grid gap-[3px]"
          style={{
            gridTemplateColumns: `repeat(${width}, 42px)`
          }}
          onMouseLeave={() => setIsDrawing(false)}
        >
          {Array.from({ length: width * height }).map((_, i) => {
            const x = i % width;
            const y = Math.floor(i / width);

            const isObstacle = obstacles.some(o => o.x === x && o.y === y);
            const isPath = animatedPath.some(p => p[0] === x && p[1] === y);
            const isRobot =
              animatedPath.length > 0 &&
              animatedPath[animatedPath.length - 1][0] === x &&
              animatedPath[animatedPath.length - 1][1] === y;

            return (
              <div
                key={i}
                onMouseDown={() => {
                  setIsDrawing(true);
                  toggleObstacle(x, y);
                }}
                onMouseUp={() => setIsDrawing(false)}
                onMouseEnter={() => {
                  if (isDrawing) toggleObstacle(x, y);
                }}
                className="w-10 h-10 rounded-md shadow-sm flex items-center justify-center cursor-pointer transition-all duration-200"
                style={{
                  backgroundColor:
                    isObstacle ? "#111827" :   // dark
                    isRobot ? "#f97316" :      // orange robot
                    isPath ? "#86efac" :       // light green
                    "#f9fafb",                // background
                  transform: isRobot ? "scale(1.1)" : "scale(1)"
                }}
              >
                {isRobot ? "🤖" : ""}
              </div>
            );
          })}
        </div>

      </div>
    </div>
  );
}