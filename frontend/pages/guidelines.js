import { useState } from 'react';
import Layout from '../components/Layout';
import Card from '../components/Card';

const TABS = ['Nutrition', 'Exercise', 'Sleep', 'Stress', 'Prevention'];

const tabContent = {
  Nutrition: (
    <div>
      <h2 style={{ marginBottom: '1rem' }}>🍎 Nutrition Guidelines</h2>

      <h3 style={{ marginBottom: '0.5rem', color: '#0077b6' }}>Balanced Diet Components</h3>
      <ol style={{ paddingLeft: '1.5rem', lineHeight: '2', color: '#444' }}>
        <li><strong>Fruits &amp; Vegetables</strong> (5 servings/day) – vitamins, minerals, fiber.</li>
        <li><strong>Whole Grains</strong> (6 servings/day) – brown rice, oats, whole-wheat bread.</li>
        <li><strong>Protein</strong> (1.6–2.2 g per kg body weight) – lean meat, fish, eggs, legumes.</li>
        <li><strong>Dairy</strong> (2–3 servings/day) – milk, yogurt, cheese.</li>
        <li><strong>Healthy Fats</strong> – olive oil, avocados, nuts (limit saturated fats &lt; 10% calories).</li>
      </ol>

      <h3 style={{ margin: '1rem 0 0.5rem', color: '#0077b6' }}>Foods to Limit</h3>
      <ul style={{ paddingLeft: '1.5rem', lineHeight: '2', color: '#444' }}>
        <li>Sugary drinks &amp; snacks</li>
        <li>Processed meats</li>
        <li>High-sodium foods</li>
        <li>Excessive caffeine</li>
      </ul>

      <h3 style={{ margin: '1rem 0 0.5rem', color: '#0077b6' }}>Hydration</h3>
      <p style={{ color: '#444', lineHeight: '1.8' }}>
        Drink at least 8 glasses (2 litres) of water per day. Increase intake during exercise, hot weather, or illness.
        Herbal teas and water-rich fruits (cucumbers, watermelon) also contribute to daily fluid intake.
      </p>

      <h3 style={{ margin: '1rem 0 0.5rem', color: '#0077b6' }}>Meal Timing Tips</h3>
      <ul style={{ paddingLeft: '1.5rem', lineHeight: '2', color: '#444' }}>
        <li>Eat breakfast within 2 hours of waking up.</li>
        <li>Avoid heavy meals within 2–3 hours of bedtime.</li>
        <li>Aim for 3 balanced meals and 1–2 healthy snacks per day.</li>
        <li>Practice mindful eating — eat slowly and without distractions.</li>
      </ul>
    </div>
  ),
  Exercise: (
    <div>
      <h2 style={{ marginBottom: '1rem' }}>🏃 Exercise Guidelines</h2>

      <h3 style={{ marginBottom: '0.5rem', color: '#0077b6' }}>WHO Recommendations (18–65 yrs)</h3>
      <ol style={{ paddingLeft: '1.5rem', lineHeight: '2', color: '#444' }}>
        <li><strong>Aerobic Activity</strong> – 150–300 min/week (brisk walking, running, cycling, swimming).</li>
        <li><strong>Strength Training</strong> – 2 days/week (weight lifting, body-weight exercises).</li>
        <li><strong>Flexibility</strong> – daily (stretching, yoga).</li>
      </ol>

      <h3 style={{ margin: '1rem 0 0.5rem', color: '#0077b6' }}>Tips for Success</h3>
      <ul style={{ paddingLeft: '1.5rem', lineHeight: '2', color: '#444' }}>
        <li>Start slowly, increase intensity gradually.</li>
        <li>Exercise with a friend for motivation.</li>
        <li>Choose activities you enjoy.</li>
        <li>Rest 1–2 days/week.</li>
        <li>Warm-up before &amp; cool-down after every session.</li>
      </ul>

      <h3 style={{ margin: '1rem 0 0.5rem', color: '#0077b6' }}>Recommended Activities by Intensity</h3>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem', marginTop: '0.5rem' }}>
        {[
          { level: 'Light', color: '#e6f7ff', border: '#b3e0f7', items: ['Walking', 'Light yoga', 'Casual cycling', 'Household chores'] },
          { level: 'Moderate', color: '#fff8e1', border: '#ffe082', items: ['Brisk walking', 'Dancing', 'Doubles tennis', 'Leisurely swimming'] },
          { level: 'Vigorous', color: '#fce8e8', border: '#f48fb1', items: ['Running', 'HIIT', 'Singles tennis', 'Competitive sports'] },
        ].map(({ level, color, border, items }) => (
          <div key={level} style={{ background: color, border: `1px solid ${border}`, borderRadius: '8px', padding: '0.75rem' }}>
            <strong style={{ display: 'block', marginBottom: '0.5rem' }}>{level}</strong>
            <ul style={{ paddingLeft: '1rem', margin: 0, fontSize: '0.9rem', color: '#444' }}>
              {items.map((item) => <li key={item}>{item}</li>)}
            </ul>
          </div>
        ))}
      </div>
    </div>
  ),
  Sleep: (
    <div>
      <h2 style={{ marginBottom: '1rem' }}>😴 Sleep Guidelines</h2>

      <h3 style={{ marginBottom: '0.5rem', color: '#0077b6' }}>Recommended Sleep Duration</h3>
      <ul style={{ paddingLeft: '1.5rem', lineHeight: '2', color: '#444' }}>
        <li><strong>Adults (18–64 yrs)</strong>: 7–9 hrs/night</li>
        <li><strong>Older Adults (65+ yrs)</strong>: 7–8 hrs/night</li>
      </ul>

      <h3 style={{ margin: '1rem 0 0.5rem', color: '#0077b6' }}>Tips for Better Sleep</h3>
      <ol style={{ paddingLeft: '1.5rem', lineHeight: '2', color: '#444' }}>
        <li><strong>Consistent Schedule</strong> – same bedtime &amp; wake-time every day.</li>
        <li><strong>Sleep Environment</strong> – dark, cool (16–19°C), quiet.</li>
        <li><strong>Pre-sleep Routine</strong> – avoid screens 1 hr before bed, relaxation, no caffeine after 2 PM.</li>
        <li><strong>Lifestyle Habits</strong> – regular exercise (not too close to bedtime), limit naps to 20–30 min, avoid alcohol/heavy meals.</li>
      </ol>

      <h3 style={{ margin: '1rem 0 0.5rem', color: '#0077b6' }}>Signs of Sleep Disorder</h3>
      <ul style={{ paddingLeft: '1.5rem', lineHeight: '2', color: '#444' }}>
        <li>Persistent insomnia</li>
        <li>Excessive daytime sleepiness</li>
        <li>Snoring or breathing interruptions</li>
        <li>Consult a doctor if issues persist more than 3 weeks</li>
      </ul>

      <h3 style={{ margin: '1rem 0 0.5rem', color: '#0077b6' }}>Sleep Hygiene Checklist</h3>
      {['Keep the bedroom for sleep only', 'Use blackout curtains or an eye mask', 'Set your thermostat to 18–20°C', 'Use white noise if needed', 'Avoid alcohol within 3 hrs of bedtime'].map((item) => (
        <div key={item} style={{ background: '#e6f7ff', borderRadius: '6px', padding: '0.5rem 0.75rem', marginBottom: '0.4rem', fontSize: '0.9rem', color: '#1a3a52' }}>
          ✓ {item}
        </div>
      ))}
    </div>
  ),
  Stress: (
    <div>
      <h2 style={{ marginBottom: '1rem' }}>🧘 Stress Management</h2>

      <h3 style={{ marginBottom: '0.5rem', color: '#0077b6' }}>Stress Management Techniques</h3>
      <ol style={{ paddingLeft: '1.5rem', lineHeight: '2', color: '#444' }}>
        <li><strong>Mindfulness &amp; Meditation</strong> – 10–20 min daily.</li>
        <li><strong>Physical Activity</strong> – releases endorphins, reduces cortisol.</li>
        <li><strong>Breathing Exercises</strong> – 4-4-4 pattern (box breathing), 5–10 min daily.</li>
        <li><strong>Time Management</strong> – prioritize tasks, break projects into steps, take regular breaks.</li>
        <li><strong>Social Connection</strong> – spend time with friends/family, join clubs.</li>
        <li><strong>Professional Help</strong> – consult a therapist if stress feels overwhelming.</li>
      </ol>

      <h3 style={{ margin: '1rem 0 0.5rem', color: '#0077b6' }}>Quick Stress Relief Techniques</h3>
      {[
        { title: '4-7-8 Breathing', desc: 'Inhale 4s, hold 7s, exhale 8s. Repeat 4 times.' },
        { title: 'Progressive Muscle Relaxation', desc: 'Tense then relax each muscle group from toes to head.' },
        { title: '5-4-3-2-1 Grounding', desc: 'Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.' },
        { title: 'Cold Water', desc: 'Splash cold water on your face to trigger the mammalian dive reflex.' },
      ].map(({ title, desc }) => (
        <div key={title} style={{ background: '#f0e6ff', border: '1px solid #d9b8ff', borderRadius: '8px', padding: '0.75rem 1rem', marginBottom: '0.5rem' }}>
          <strong style={{ color: '#6c3483' }}>{title}</strong>
          <p style={{ margin: '0.25rem 0 0', fontSize: '0.9rem', color: '#555' }}>{desc}</p>
        </div>
      ))}

      <h3 style={{ margin: '1rem 0 0.5rem', color: '#0077b6' }}>Signs You Need Professional Help</h3>
      <ul style={{ paddingLeft: '1.5rem', lineHeight: '2', color: '#444' }}>
        <li>Stress interferes with daily life for more than 2 weeks</li>
        <li>Using alcohol or substances to cope</li>
        <li>Feeling hopeless, worthless, or having thoughts of self-harm</li>
        <li>Physical symptoms (chest pain, severe headaches) with no medical cause</li>
      </ul>
    </div>
  ),
  Prevention: (
    <div>
      <h2 style={{ marginBottom: '1rem' }}>🛡️ Disease Prevention</h2>

      <h3 style={{ marginBottom: '0.5rem', color: '#0077b6' }}>Prevention Strategies</h3>
      <ol style={{ paddingLeft: '1.5rem', lineHeight: '2', color: '#444' }}>
        <li><strong>Cardiovascular Health</strong> – maintain BMI 18.5–24.9, control BP &amp; cholesterol, limit salt &lt; 5 g/day.</li>
        <li><strong>Diabetes Prevention</strong> – healthy weight, regular exercise, whole grains, reduce sugar.</li>
        <li><strong>Cancer Prevention</strong> – avoid tobacco &amp; excess alcohol, plenty of fruits/veg, regular screenings.</li>
        <li><strong>Regular Check-ups</strong> – annual health screening, dental check-up every 6 months, vision check as needed.</li>
        <li><strong>Vaccination</strong> – seasonal flu vaccine annually; follow recommended schedule.</li>
        <li><strong>Mental Health</strong> – regular exercise, good sleep, social connections, seek help when needed.</li>
      </ol>

      <h3 style={{ margin: '1rem 0 0.5rem', color: '#0077b6' }}>Recommended Screenings by Age</h3>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
          <thead>
            <tr style={{ background: '#e6f7ff' }}>
              {['Screening', '20s', '30s', '40s', '50s+'].map((h) => (
                <th key={h} style={{ padding: '0.5rem 0.75rem', textAlign: 'left', color: '#0077b6' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {[
              ['Blood Pressure', 'Every 2 yrs', 'Every 2 yrs', 'Every year', 'Every year'],
              ['Blood Sugar', 'Every 3 yrs', 'Every 3 yrs', 'Every 3 yrs', 'Every year'],
              ['Cholesterol', 'Every 5 yrs', 'Every 5 yrs', 'Every 5 yrs', 'Every 1-2 yrs'],
              ['Vision', 'Every 2 yrs', 'Every 2 yrs', 'Every 2 yrs', 'Every year'],
              ['Dental', 'Every 6 mo', 'Every 6 mo', 'Every 6 mo', 'Every 6 mo'],
            ].map((row, i) => (
              <tr key={row[0]} style={{ background: i % 2 === 0 ? '#fff' : '#f8fbff' }}>
                {row.map((cell, j) => (
                  <td key={j} style={{ padding: '0.5rem 0.75rem', color: '#444' }}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  ),
};

export default function GuidelinesPage() {
  const [activeTab, setActiveTab] = useState('Nutrition');

  return (
    <Layout>
      <h1>📚 Health Guidelines &amp; Tips</h1>
      <p style={{ color: '#888', marginBottom: '1.5rem' }}>
        Evidence-based recommendations to support a healthy lifestyle.
      </p>

      {/* Tab bar */}
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1.5rem' }}>
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              padding: '0.5rem 1.25rem',
              borderRadius: '20px',
              border: activeTab === tab ? '2px solid #0077b6' : '1px solid #ddd',
              background: activeTab === tab ? '#0077b6' : '#fff',
              color: activeTab === tab ? '#fff' : '#555',
              fontWeight: activeTab === tab ? '600' : '400',
              cursor: 'pointer',
              fontSize: '0.9rem',
              transition: 'all 0.15s',
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      <Card>
        {tabContent[activeTab]}
      </Card>

      <p style={{ color: '#aaa', fontSize: '0.85rem', textAlign: 'center', marginTop: '1rem' }}>
        ⚠️ Disclaimer: This information is for educational purposes only and does not replace professional medical advice.
        Always consult a qualified healthcare provider before making changes to your health routine.
      </p>
    </Layout>
  );
}
