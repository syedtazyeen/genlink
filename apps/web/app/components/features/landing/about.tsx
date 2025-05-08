import { useState } from "react";

const features = [
  {
    key: "workflows",
    title: "Routine Tasks",
    icon: "",
    description:
      "Automate routine tasks, from note-taking to report generation, with AI that adapts to your flow. Save time and focus on what matters most.",
  },
  {
    key: "creative",
    title: "Whiteboards",
    icon: "",
    description:
      "Use interactive, AI-powered whiteboards to brainstorm, prototype, and refine ideas visually. Built for creators, thinkers, and fast movers.",
  },
  {
    key: "learning",
    title: "Agentic Memory",
    icon: "",
    description:
      "Learn smarter, not harder. Personalized suggestions and AI-driven assistance help you grasp concepts faster and grow continuously.",
  },
];

export default function About() {
  const [selected, setSelected] = useState("workflows");
  const activeFeature = features.find((f) => f.key === selected);

  return (
    <div
      id="about"
      className="w-full max-w-6xl mx-auto py-20 px-4 text-center font-brand"
    >
      <h1 className="text-4xl leading-tight max-w-lg mx-auto tracking-tighter">
        Empowering Minds, Accelerating Progress
      </h1>
      <p className="mt-2 text-md font-light max-w-xl mx-auto text-muted-foreground tracking-wider">
        Our intelligent workspace evolves with you — helping you think, create,
        and learn at the speed of thought.
      </p>

      <div className="flex justify-center gap-4 flex-wrap mt-12 mb-6">
        {features.map((feature) => (
          <button
            key={feature.key}
            onClick={() => setSelected(feature.key)}
            className={`px-4 py-2 rounded-md text-sm transition ${
              selected === feature.key
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground"
            }`}
          >
            {feature.icon} {feature.title}
          </button>
        ))}
      </div>

      {activeFeature && (
        <div className="max-w-5xl h-64 mx-auto text-left bg-background rounded-md">
          <div className="w-1/2 space-y-2 h-full flex flex-col justify-center">
            <h3 className="text-2xl tracking-tight">{activeFeature.title}</h3>
            <p className="text-muted-foreground text-base font-light tracking-wide">
              {activeFeature.description}
            </p>
          </div>
          <div></div>
        </div>
      )}
    </div>
  );
}
