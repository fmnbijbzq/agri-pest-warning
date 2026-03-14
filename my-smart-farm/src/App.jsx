import React, { useState, useEffect, useRef } from 'react';
import { 
  MapPin, CloudRain, Droplets, Thermometer, Mic, Send, Menu, 
  BarChart2, Map, Settings, User, AlertTriangle, ChevronDown,
  TrendingUp, ShieldCheck, Cpu, RefreshCw, AlertCircle, Play, 
  Pause, Sliders, Database, Activity, CheckCircle2, Terminal,
  Sparkles
} from 'lucide-react';

// --- 全局 Gemini API 调用工具函数 ---
const callGeminiAPI = async (prompt) => {
  const apiKey = ""; // 执行环境会在运行时自动注入 API Key
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`;
  
  const payload = {
    contents: [{ parts: [{ text: prompt }] }],
    systemInstruction: {
      parts: [{
        text: "你是一个专业的农业植保专家和灾害数据分析师。回答尽量简明扼要，使用纯文本格式，避免使用复杂的 Markdown 语法（可以适当使用换行和标点符号），语言专业且富有同理心。"
      }]
    }
  };

  let delay = 1000;
  for (let i = 0; i < 5; i++) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      return data.candidates?.[0]?.content?.parts?.[0]?.text || "抱歉，目前 AI 模型思考遇到了点问题，请稍后再试。";
    } catch (e) {
      if (i === 4) return "⚠️ AI 服务连接失败，请检查网络或稍后再试。";
      await new Promise(r => setTimeout(r, delay));
      delay *= 2; // 指数退避重试
    }
  }
};

// --- 共用组件：加载骨架屏 ---
const SkeletonLoader = ({ text }) => (
  <div className="flex flex-col items-center justify-center p-6 space-y-4 animate-pulse">
    <RefreshCw className="w-8 h-8 text-emerald-500 animate-spin" />
    <div className="text-sm font-medium text-emerald-600/80 bg-emerald-50 px-4 py-2 rounded-full shadow-inner">
      {text || "正在处理海量数据..."}
    </div>
  </div>
);

// ==========================================
// 界面一：移动端极简版 (面向农户) - ✨ 已接入 Gemini API
// ==========================================
const MobileView = () => {
  const [messages, setMessages] = useState([
    { id: 1, type: 'system', text: '您好！我是您的智慧农卫士，基于 Gemini 农业大模型为您提供决策建议。' },
    { id: 2, type: 'system', text: '⚠️ 预警播报：根据近期高湿高温天气及预测模型，本地水稻爆发稻瘟病概率极高（85%）。建议在放晴后 48 小时内进行喷洒作业。您可以向我提问关于农药、防治等任何问题。' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async (text) => {
    const userMsg = text || input;
    if (!userMsg) return;
    
    // 更新 UI，显示用户消息
    setMessages(prev => [...prev, { id: Date.now(), type: 'user', text: userMsg }]);
    setInput('');
    setIsTyping(true);

    // 构建上下文 Prompt 给 Gemini
    const prompt = `当前环境上下文：用户位于湖南省长沙市，当前天气连续暴雨，湿度88%，温度28°C。系统刚向用户发送了水稻稻瘟病高发预警。
用户提问：${userMsg}
请以“智慧农卫士”的身份，用亲切、易懂（适合农民阅读）的中文给出现实可行的农业指导建议。不要太长，控制在150字以内。`;

    const responseText = await callGeminiAPI(prompt);

    setIsTyping(false);
    setMessages(prev => [...prev, { 
      id: Date.now() + 1, type: 'system', 
      text: responseText 
    }]);
  };

  return (
    <div className="flex justify-center items-center py-8 bg-gray-100 min-h-screen">
      <div className="w-[375px] h-[812px] bg-gray-50 rounded-[3rem] shadow-2xl border-8 border-gray-900 overflow-hidden flex flex-col relative">
        {/* 顶部导航 */}
        <div className={`bg-emerald-600 text-white px-5 pt-12 pb-4 shadow-md z-10 rounded-b-3xl`}>
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-xl font-bold tracking-wider flex items-center gap-2">
              <ShieldCheck className="w-6 h-6"/> 智慧农卫士 <Sparkles className="w-4 h-4 text-yellow-300"/>
            </h1>
          </div>
          <div className="inline-flex items-center gap-1 bg-white/20 px-3 py-1.5 rounded-full text-sm font-medium backdrop-blur-sm cursor-pointer">
            <MapPin className="w-4 h-4"/> 湖南省·长沙市 <ChevronDown className="w-4 h-4"/>
          </div>
        </div>

        {/* 状态卡片 */}
        <div className="px-5 -mt-4 pt-8 z-0 shrink-0">
          <div className="bg-white rounded-2xl p-4 shadow-lg border border-gray-100 mb-4">
            <div className="flex justify-between items-center text-sm text-gray-600 mb-4 pb-4 border-b border-gray-100">
              <span className="flex items-center gap-1 font-medium"><CloudRain className="w-4 h-4 text-blue-500"/> 连续暴雨</span>
              <span className="flex items-center gap-1"><Droplets className="w-4 h-4 text-cyan-500"/> 88%</span>
              <span className="flex items-center gap-1"><Thermometer className="w-4 h-4 text-orange-500"/> 28°C</span>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-gray-500 text-sm mb-1">当前综合风险</h2>
                <div className="text-2xl font-bold text-gray-800">极高风险状态</div>
              </div>
              <div className="relative w-20 h-20">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="40" stroke="#f3f4f6" strokeWidth="10" fill="none" />
                  <circle cx="50" cy="50" r="40" stroke="#D32F2F" strokeWidth="10" fill="none" strokeDasharray="251" strokeDashoffset="37.65" className="transition-all duration-1000 ease-out" />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center flex-col">
                  <span className="text-red-600 font-bold text-xl">85%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* AI 对话区 */}
        <div className="flex-1 overflow-y-auto px-5 pb-32 space-y-4 pt-2">
          {messages.map(msg => (
            <div key={msg.id} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[85%] p-3.5 rounded-2xl shadow-sm text-[15px] leading-relaxed whitespace-pre-wrap ${
                msg.type === 'user' ? `bg-emerald-600 text-white rounded-tr-sm` : `bg-white border border-gray-100 text-gray-800 rounded-tl-sm`
              }`}>
                {msg.text}
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-100 p-3 rounded-2xl rounded-tl-sm shadow-sm flex gap-1">
                <div className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                <div className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* 底部输入框 */}
        <div className="absolute bottom-0 w-full bg-white/90 backdrop-blur-md border-t border-gray-100 px-4 py-4 pb-8">
          <div className="flex gap-2 overflow-x-auto pb-3 scrollbar-hide">
            {['推荐农药配比', '最佳打药时间', '如何识别早期病斑'].map((chip) => (
              <button 
                key={chip} 
                onClick={() => handleSend(chip)} 
                disabled={isTyping}
                className="whitespace-nowrap px-4 py-1.5 bg-emerald-50 text-emerald-700 rounded-full text-sm font-medium border border-emerald-100 disabled:opacity-50"
              >
                {chip}
              </button>
            ))}
          </div>
          <div className="flex items-center gap-3">
            <button className="p-3 bg-gray-100 text-gray-600 rounded-full"><Mic className="w-5 h-5" /></button>
            <input 
              type="text" 
              value={input} 
              onChange={(e) => setInput(e.target.value)} 
              onKeyPress={(e) => e.key === 'Enter' && !isTyping && handleSend()}
              placeholder="描述田间情况或提问..." 
              disabled={isTyping}
              className="flex-1 bg-gray-100 text-[16px] px-4 py-3 rounded-full focus:outline-none focus:ring-2 focus:ring-emerald-500 disabled:opacity-50"
            />
            <button 
              onClick={() => handleSend()} 
              disabled={isTyping || !input.trim()}
              className="p-3 bg-emerald-600 text-white rounded-full shadow-lg disabled:bg-gray-400 transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};


// ==========================================
// PC 端子页面 1：综合预警大屏 (Dashboard) - ✨ 已接入 Gemini API 动态分析
// ==========================================
const DashboardTab = () => {
  const [insightText, setInsightText] = useState("宏观分析：根据当前气象与预测模型，受副热带高压边缘及连续暴雨影响，长沙县及芙蓉区形成典型“高温高湿”微气候，模型判定其为水稻稻瘟病爆发的极佳温床。建议立即拉响红色预警并调配无人机防飞队伍。");
  const [isGeneratingInsight, setIsGeneratingInsight] = useState(false);

  const generateAIInsight = async () => {
    setIsGeneratingInsight(true);
    const prompt = `你是一个服务于政府农业部门的“AI防灾减灾总架构师”。
当前辖区监测数据如下：
- 本周新增预警区域：124个（较上周上升15%）
- 高风险作物预估面积：35,000亩
- XGBoost模型预测置信度：92.4%
- 核心风险点：长沙县、芙蓉区受连续降雨和高温影响，水稻稻瘟病爆发概率超90%。

请根据上述数据，生成一段约120字的“AI辅助决策洞察分析”，语气必须客观、专业、有政府公文风格。直接输出分析内容，不要任何寒暄词，不要分点，写成一段或两段。`;

    const responseText = await callGeminiAPI(prompt);
    setInsightText(responseText);
    setIsGeneratingInsight(false);
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* KPI 行 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-red-50 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-110"></div>
          <h3 className="text-gray-500 text-sm font-medium mb-2">本周新增预警区域数</h3>
          <div className="flex items-end gap-3">
            <span className="text-4xl font-bold text-gray-800">124</span>
            <span className="flex items-center text-sm font-bold text-red-500 bg-red-50 px-2 py-0.5 rounded text-red-600">
              <TrendingUp className="w-3 h-3 mr-1" /> 15%
            </span>
          </div>
        </div>
        <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-orange-50 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-110"></div>
          <h3 className="text-gray-500 text-sm font-medium mb-2">高风险作物面积预估</h3>
          <div className="flex items-end gap-3">
            <span className="text-4xl font-bold text-gray-800">35,000</span><span className="text-gray-500 mb-1">亩</span>
          </div>
        </div>
        <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-50 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-110"></div>
          <h3 className="text-gray-500 text-sm font-medium mb-2">XGBoost 模型置信度</h3>
          <div className="flex items-center justify-between">
            <div className="flex items-end gap-2"><span className="text-4xl font-bold text-gray-800">92.4</span><span className="text-gray-500 mb-1">%</span></div>
            <Cpu className="w-8 h-8 text-emerald-500 opacity-80" />
          </div>
        </div>
      </div>

      {/* 中层图表 */}
      <div className="grid grid-cols-1 lg:grid-cols-10 gap-6">
        <div className="lg:col-span-6 bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex flex-col h-[400px]">
          <h3 className="text-lg font-bold text-gray-800 mb-4">📍 辖区病虫害风险热力图</h3>
          <div className="flex-1 bg-gray-50 rounded-lg border border-gray-200 overflow-hidden relative flex items-center justify-center">
            <div className="grid grid-cols-4 gap-2 w-full max-w-[500px] p-4">
              {[ { name: '芙蓉区', risk: 'high', color: 'bg-red-500/80' }, { name: '天心区', risk: 'mid', color: 'bg-orange-400/80' }, { name: '岳麓区', risk: 'low', color: 'bg-emerald-400/80' }, { name: '开福区', risk: 'mid', color: 'bg-orange-400/80' }, { name: '雨花区', risk: 'high', color: 'bg-red-500/80' }, { name: '望城区', risk: 'low', color: 'bg-emerald-400/80' }, { name: '长沙县', risk: 'high', color: 'bg-red-600/90' }, { name: '浏阳市', risk: 'low', color: 'bg-emerald-400/80' }
              ].map((area, i) => (
                 <div key={i} className={`${area.color} h-24 rounded-md flex flex-col items-center justify-center text-white shadow-sm transition-transform hover:scale-105 cursor-pointer`}>
                    <span className="font-bold text-sm drop-shadow-md">{area.name}</span>
                    {area.risk === 'high' && <AlertCircle className="w-4 h-4 mt-1 opacity-80" />}
                 </div>
              ))}
            </div>
          </div>
        </div>
        <div className="lg:col-span-4 bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex flex-col h-[400px]">
            <h3 className="text-lg font-bold text-gray-800 mb-4">📈 气象-患病概率预测趋势</h3>
            <div className="flex-1 w-full flex items-end relative pb-8 pl-8 pt-4">
              <div className="absolute left-0 top-0 bottom-8 flex flex-col justify-between text-xs text-blue-500 font-medium">
                <span>150mm</span><span>100mm</span><span>50mm</span><span>0</span>
              </div>
              <div className="absolute right-0 top-0 bottom-8 flex flex-col justify-between text-xs text-red-500 font-medium text-right">
                <span>100%</span><span>50%</span><span>0%</span>
              </div>
              <svg className="w-full h-full overflow-visible" preserveAspectRatio="none">
                <line x1="0" y1="0" x2="100%" y2="0" stroke="#f3f4f6" strokeWidth="1" />
                <line x1="0" y1="50%" x2="100%" y2="50%" stroke="#f3f4f6" strokeWidth="1" />
                <line x1="0" y1="100%" x2="100%" y2="100%" stroke="#e5e7eb" strokeWidth="2" />
                
                <rect x="5%" y="60%" width="10%" height="40%" fill="#3b82f6" opacity="0.3" rx="2" />
                <rect x="25%" y="40%" width="10%" height="60%" fill="#3b82f6" opacity="0.5" rx="2" />
                <rect x="45%" y="20%" width="10%" height="80%" fill="#3b82f6" opacity="0.6" rx="2" />
                <rect x="65%" y="10%" width="10%" height="90%" fill="#3b82f6" opacity="0.8" rx="2" />
                <rect x="85%" y="30%" width="10%" height="70%" fill="#3b82f6" opacity="0.5" rx="2" />
  
                <polyline points="10%,80% 30%,70% 50%,30% 70%,10% 90%,15%" fill="none" stroke="#ef4444" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
                <circle cx="70%" cy="10%" r="5" fill="#ef4444" stroke="#fff" strokeWidth="2" className="animate-pulse" />
              </svg>
              <div className="absolute bottom-0 left-8 right-0 flex justify-between text-xs text-gray-500">
                <span className="ml-[2%]">周一</span><span className="ml-[6%]">周二</span><span className="ml-[8%]">周三</span><span className="ml-[8%] font-bold text-red-500">周四(爆)</span><span className="ml-[4%]">周五</span>
              </div>
            </div>
        </div>
      </div>

      {/* 底部 AI 洞察报告 */}
      <div className="bg-white rounded-xl shadow-sm border border-emerald-200 p-6 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-1 h-full bg-emerald-500"></div>
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-bold text-emerald-800 flex items-center gap-2">
            <Cpu className="w-5 h-5" /> Gemini AI 实时决策洞察报告
          </h3>
          <button 
            onClick={generateAIInsight}
            disabled={isGeneratingInsight}
            className="flex items-center gap-2 px-4 py-2 bg-emerald-50 text-emerald-700 hover:bg-emerald-100 rounded-lg text-sm font-bold transition-colors disabled:opacity-50 border border-emerald-200"
          >
            {isGeneratingInsight ? <RefreshCw className="w-4 h-4 animate-spin"/> : <Sparkles className="w-4 h-4" />}
            {isGeneratingInsight ? 'AI 深度运算中...' : '✨ 一键生成报告'}
          </button>
        </div>
        
        {isGeneratingInsight ? (
          <div className="py-4 space-y-3">
            <div className="h-4 bg-gray-200 rounded animate-pulse w-full"></div>
            <div className="h-4 bg-gray-200 rounded animate-pulse w-11/12"></div>
            <div className="h-4 bg-gray-200 rounded animate-pulse w-4/5"></div>
          </div>
        ) : (
          <div className="prose prose-sm text-gray-700 leading-relaxed max-w-none whitespace-pre-wrap p-4 bg-emerald-50/50 rounded-lg border border-emerald-50">
            {insightText}
          </div>
        )}
      </div>
    </div>
  );
};

// ==========================================
// PC 端子页面 2：历史病虫害 GIS (GIS Map)
// ==========================================
const GISView = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [month, setMonth] = useState(3);

  useEffect(() => {
    let interval;
    if (isPlaying) {
      interval = setInterval(() => {
        setMonth(m => m >= 10 ? 3 : m + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isPlaying]);

  return (
    <div className="space-y-6 animate-fadeIn flex flex-col h-[calc(100vh-140px)]">
      {/* 顶部过滤器 */}
      <div className="bg-white p-4 rounded-xl border border-gray-100 shadow-sm flex items-center justify-between">
        <div className="flex gap-4">
          <select className="border border-gray-200 rounded-lg px-4 py-2 text-sm bg-gray-50 focus:outline-none focus:ring-2 focus:ring-emerald-500">
            <option>2023-2024 跨年周期</option>
            <option>2022-2023 跨年周期</option>
          </select>
          <select className="border border-gray-200 rounded-lg px-4 py-2 text-sm bg-gray-50 focus:outline-none focus:ring-2 focus:ring-emerald-500">
            <option>病害：稻瘟病 (Rice Blast)</option>
            <option>虫害：草地贪夜蛾</option>
          </select>
        </div>
        <div className="flex items-center gap-2 text-sm font-medium text-gray-600">
          <span>空间聚类模式:</span>
          <button className="bg-emerald-100 text-emerald-700 px-3 py-1 rounded-md">热力图</button>
          <button className="hover:bg-gray-100 px-3 py-1 rounded-md">散点图</button>
        </div>
      </div>

      {/* GIS 主体 */}
      <div className="flex-1 bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden relative flex">
        {/* 左侧地图区 */}
        <div className="flex-1 bg-[#F8FAFC] relative overflow-hidden flex items-center justify-center p-8">
          {/* 模拟 GIS 网格底图 */}
          <div className="absolute inset-0 opacity-10 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCI+CjxwYXRoIGQ9Ik0wLDBMNDAsNDBNNDAsMEwwLDQwIiBzdHJva2U9IiMzMzMiIHN0cm9rZS13aWR0aD0iMC41Ii8+PC9zdmc+')]"></div>
          
          {/* 手工绘制的矢量地图模拟 */}
          <svg viewBox="0 0 800 600" className="w-full h-full max-w-4xl drop-shadow-2xl">
            <defs>
              <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="8" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
              </filter>
            </defs>
            {/* 虚拟地块 */}
            <path d="M100,100 L300,50 L450,200 L250,350 Z" fill="#E2E8F0" stroke="#CBD5E1" strokeWidth="2" />
            <path d="M300,50 L600,80 L700,250 L450,200 Z" fill="#E2E8F0" stroke="#CBD5E1" strokeWidth="2" />
            <path d="M450,200 L700,250 L650,500 L350,450 Z" fill="#E2E8F0" stroke="#CBD5E1" strokeWidth="2" />
            <path d="M100,100 L250,350 L350,450 L150,550 Z" fill="#E2E8F0" stroke="#CBD5E1" strokeWidth="2" />
            
            {/* 随时间变化的疫情散点 */}
            {month >= 4 && <circle cx="200" cy="200" r={month*2} fill="rgba(239, 68, 68, 0.4)" filter="url(#glow)" />}
            {month >= 5 && <circle cx="500" cy="150" r={(month-2)*3} fill="rgba(249, 115, 22, 0.5)" filter="url(#glow)" />}
            {month >= 6 && <circle cx="550" cy="350" r={(month-4)*4} fill="rgba(239, 68, 68, 0.6)" filter="url(#glow)" />}
            {month >= 7 && <circle cx="300" cy="400" r={(month-5)*5} fill="rgba(220, 38, 38, 0.7)" filter="url(#glow)" />}
            
            {/* 核心爆发中心 */}
            <circle cx="550" cy="350" r="6" fill="#7F1D1D" />
            <circle cx="300" cy="400" r="6" fill="#7F1D1D" />
            <text x="560" y="340" fontSize="14" fill="#475569" fontWeight="bold">芙蓉区 (核心发病区)</text>
          </svg>

          {/* 底部时间轴控制 */}
          <div className="absolute bottom-8 left-1/2 -translate-x-1/2 bg-white/90 backdrop-blur-md px-6 py-4 rounded-2xl shadow-xl border border-gray-200 flex items-center gap-6 w-3/4 max-w-2xl z-10">
            <button onClick={() => setIsPlaying(!isPlaying)} className="w-12 h-12 bg-emerald-600 hover:bg-emerald-700 text-white rounded-full flex items-center justify-center shadow-lg transition-transform hover:scale-105">
              {isPlaying ? <Pause className="w-6 h-6" /> : <Play className="w-6 h-6 ml-1" />}
            </button>
            <div className="flex-1 relative">
              <div className="h-2 bg-gray-200 rounded-full w-full"></div>
              <div className="absolute top-0 left-0 h-2 bg-emerald-500 rounded-full transition-all duration-300" style={{ width: `${((month-3)/7)*100}%` }}></div>
              <div className="flex justify-between mt-2 text-xs font-medium text-gray-500">
                <span>3月</span><span>4月</span><span>5月</span><span>6月</span><span>7月</span><span>8月</span><span>9月</span><span>10月</span>
              </div>
            </div>
            <div className="text-2xl font-black text-emerald-800 tracking-tighter w-16 text-right">
              {month}月
            </div>
          </div>
        </div>

        {/* 右侧数据面板 */}
        <div className="w-80 border-l border-gray-100 bg-white p-5 flex flex-col gap-6 overflow-y-auto">
          <div>
            <h4 className="font-bold text-gray-800 flex items-center gap-2 mb-3"><Activity className="w-4 h-4 text-emerald-500"/> 空间演化分析</h4>
            <div className="bg-emerald-50 text-emerald-800 text-sm p-3 rounded-lg border border-emerald-100 leading-relaxed">
              基于 {month} 月数据，稻瘟病中心呈现由东北向西南呈扇形扩散趋势，扩散速率与当地主导风向（东北风）呈 0.82 强相关。
            </div>
          </div>
          <div>
            <h4 className="font-bold text-gray-800 mb-3">区域高发排名 Top 3</h4>
            <div className="space-y-3">
              {[
                { name: '芙蓉区东郊', val: '8,400亩', bar: '90%' },
                { name: '长沙县路口镇', val: '5,200亩', bar: '65%' },
                { name: '雨花区跳马镇', val: '3,100亩', bar: '40%' }
              ].map((item, i) => (
                <div key={i}>
                  <div className="flex justify-between text-sm mb-1 text-gray-600">
                    <span>{i+1}. {item.name}</span><span className="font-bold text-gray-800">{item.val}</span>
                  </div>
                  <div className="h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
                    <div className="h-full bg-red-500 rounded-full" style={{width: item.bar}}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// PC 端子页面 3：气象与模型配置 (Config & AI 中台)
// ==========================================
const ConfigView = () => {
  return (
    <div className="space-y-6 animate-fadeIn">
      {/* 模块化卡片布局 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* 左侧：IoT与气象源 */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2 mb-6">
            <Database className="w-5 h-5 text-blue-500" /> IoT传感器与气象 API 接入池
          </h3>
          <div className="space-y-4">
            {[
              { name: '国家气象局 7天预报接口', type: 'REST API', status: 'Online', ms: '42ms' },
              { name: '农田微气候土壤湿度传感器 (区A)', type: 'MQTT', status: 'Online', ms: '12ms' },
              { name: '农田微气候土壤湿度传感器 (区B)', type: 'MQTT', status: 'Offline', ms: '-' },
              { name: '高分一号多光谱卫星影像', type: 'WMS', status: 'Online', ms: '850ms' },
            ].map((node, i) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-lg border border-gray-100 bg-gray-50/50 hover:bg-gray-50 transition-colors">
                <div className="flex items-center gap-3">
                  <div className={`w-2 h-2 rounded-full ${node.status === 'Online' ? 'bg-emerald-500 shadow-[0_0_8px_#10b981]' : 'bg-red-500'}`}></div>
                  <div>
                    <div className="text-sm font-bold text-gray-700">{node.name}</div>
                    <div className="text-xs text-gray-400 font-mono">{node.type}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-xs font-bold ${node.status === 'Online' ? 'text-emerald-600' : 'text-red-500'}`}>{node.status}</div>
                  <div className="text-xs text-gray-400 font-mono">{node.ms}</div>
                </div>
              </div>
            ))}
          </div>
          <button className="w-full mt-4 py-2 bg-blue-50 text-blue-600 rounded-lg text-sm font-bold hover:bg-blue-100 transition-colors border border-blue-100">
            + 添加新数据源
          </button>
        </div>

        {/* 右侧：超参数调优面板 */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2 mb-6">
            <Sliders className="w-5 h-5 text-orange-500" /> XGBoost 引擎超参数微调
          </h3>
          <div className="space-y-6">
            <div>
              <div className="flex justify-between text-sm mb-2"><span className="text-gray-600 font-medium">n_estimators (决策树数量)</span><span className="font-mono text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">250</span></div>
              <input type="range" min="50" max="500" defaultValue="250" className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-emerald-500" />
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2"><span className="text-gray-600 font-medium">max_depth (树的最大深度)</span><span className="font-mono text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">6</span></div>
              <input type="range" min="3" max="15" defaultValue="6" className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-emerald-500" />
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2"><span className="text-gray-600 font-medium">learning_rate (学习率)</span><span className="font-mono text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">0.05</span></div>
              <input type="range" min="0.01" max="0.3" step="0.01" defaultValue="0.05" className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-emerald-500" />
            </div>
          </div>
          <div className="mt-8 flex gap-3">
            <button className="flex-1 py-2.5 bg-gray-900 text-white rounded-lg text-sm font-bold hover:bg-gray-800 shadow flex items-center justify-center gap-2">
              <RefreshCw className="w-4 h-4" /> 重新训练模型
            </button>
            <button className="px-4 py-2.5 bg-white border border-gray-200 text-gray-600 rounded-lg text-sm font-bold hover:bg-gray-50">恢复默认</button>
          </div>
        </div>
      </div>

      {/* 下排：训练控制台 & 评估图表 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-64">
        {/* 伪终端 */}
        <div className="bg-[#1E1E1E] rounded-xl shadow-sm p-4 font-mono text-xs overflow-hidden flex flex-col relative border border-gray-800">
          <div className="flex items-center gap-2 mb-3 pb-2 border-b border-gray-700">
            <Terminal className="w-4 h-4 text-gray-400" />
            <span className="text-gray-400 font-bold">Training Console output</span>
          </div>
          <div className="flex-1 overflow-y-auto space-y-1 text-green-400 opacity-90">
            <p className="text-gray-400">Loading historical dataset (n=45,210)... OK</p>
            <p className="text-gray-400">Initializing XGBClassifier...</p>
            <p>[Epoch 01/20] train-logloss: 0.61203 | val-logloss: 0.62011</p>
            <p>[Epoch 05/20] train-logloss: 0.42150 | val-logloss: 0.44520</p>
            <p>[Epoch 10/20] train-logloss: 0.28541 | val-logloss: 0.31205</p>
            <p>[Epoch 15/20] train-logloss: 0.19830 | val-logloss: 0.22010</p>
            <p className="text-emerald-300 font-bold mt-2">&gt; Training Complete. Best iteration: 18</p>
            <p className="text-emerald-300 font-bold">&gt; Model saved to registry (v2.4.1)</p>
          </div>
        </div>

        {/* 特征重要性 / ROC */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex flex-col">
          <h3 className="text-sm font-bold text-gray-800 mb-4">特征重要性 (Feature Importance)</h3>
          <div className="flex-1 flex flex-col justify-center space-y-4">
             {[
               { label: '连续3天平均湿度 (Humidity)', width: '90%', color: 'bg-emerald-500' },
               { label: '日均温差 (Temp Diff)', width: '75%', color: 'bg-emerald-400' },
               { label: '累计降雨量 (Rainfall)', width: '60%', color: 'bg-emerald-300' },
               { label: '历史病斑残留系数', width: '35%', color: 'bg-gray-300' }
             ].map((ft, i) => (
               <div key={i} className="flex items-center gap-3">
                 <div className="w-32 text-xs text-gray-500 truncate text-right">{ft.label}</div>
                 <div className="flex-1 h-3 bg-gray-100 rounded-sm overflow-hidden">
                   <div className={`h-full ${ft.color} rounded-sm`} style={{ width: ft.width }}></div>
                 </div>
               </div>
             ))}
          </div>
        </div>
      </div>
    </div>
  );
};


// ==========================================
// 主应用容器：控制端与导航切换
// ==========================================
export default function App() {
  const [viewMode, setViewMode] = useState('pc'); // 'mobile' | 'pc'
  const [pcTab, setPcTab] = useState('dashboard'); // 'dashboard' | 'gis' | 'config'

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col font-sans">
      {/* 比赛演示专用全局控制条 */}
      <div className="bg-gray-800 text-white p-3 flex justify-between items-center border-b border-gray-700 z-50 sticky top-0">
        <div className="flex items-center gap-3">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          <span className="font-bold tracking-wide">大学生计算机设计大赛 - ✨ AI 增强演示版</span>
        </div>
        <div className="flex bg-gray-900 rounded-lg p-1 border border-gray-700">
          <button 
            onClick={() => setViewMode('mobile')}
            className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${viewMode === 'mobile' ? 'bg-emerald-600 text-white shadow' : 'text-gray-400 hover:text-white'}`}
          >
            📱 农户端 (极简版)
          </button>
          <button 
            onClick={() => setViewMode('pc')}
            className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${viewMode === 'pc' ? 'bg-emerald-600 text-white shadow' : 'text-gray-400 hover:text-white'}`}
          >
            💻 监管端 (数据大屏)
          </button>
        </div>
      </div>

      {/* 视口渲染 */}
      <div className="flex-1 w-full h-full relative">
        {viewMode === 'mobile' ? (
          <MobileView />
        ) : (
          <div className="flex min-h-[calc(100vh-53px)] bg-[#F4F7F6] overflow-hidden">
            {/* PC端 左侧菜单栏 */}
            <div className="w-64 bg-[#1B3B36] text-emerald-100 flex flex-col shadow-2xl z-20 shrink-0">
              <div className="p-6 pb-8 border-b border-emerald-800">
                <div className="flex items-center gap-4 bg-emerald-900/50 p-3 rounded-xl border border-emerald-800/50 mt-4">
                  <div className="w-10 h-10 rounded-full bg-emerald-600 flex items-center justify-center text-white font-bold">王</div>
                  <div>
                    <div className="text-sm font-bold text-white">王建国</div>
                    <div className="text-xs text-emerald-300">区域植保总监</div>
                  </div>
                </div>
              </div>
              <nav className="flex-1 p-4 space-y-2">
                <button 
                  onClick={() => setPcTab('dashboard')} 
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${pcTab === 'dashboard' ? 'bg-emerald-600/20 text-white border-l-4 border-emerald-400 font-bold' : 'text-emerald-200 hover:bg-emerald-800/30 border-l-4 border-transparent'}`}
                >
                  <BarChart2 className="w-5 h-5" /> 综合预警大屏
                </button>
                <button 
                  onClick={() => setPcTab('gis')} 
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${pcTab === 'gis' ? 'bg-emerald-600/20 text-white border-l-4 border-emerald-400 font-bold' : 'text-emerald-200 hover:bg-emerald-800/30 border-l-4 border-transparent'}`}
                >
                  <Map className="w-5 h-5" /> 历史病虫害 GIS
                </button>
                <button 
                  onClick={() => setPcTab('config')} 
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${pcTab === 'config' ? 'bg-emerald-600/20 text-white border-l-4 border-emerald-400 font-bold' : 'text-emerald-200 hover:bg-emerald-800/30 border-l-4 border-transparent'}`}
                >
                  <Settings className="w-5 h-5" /> 气象与模型配置
                </button>
              </nav>
            </div>

            {/* PC端 右侧主内容区 */}
            <div className="flex-1 flex flex-col h-full overflow-y-auto">
              <header className="bg-white px-8 py-5 flex justify-between items-center shadow-sm z-10 shrink-0">
                <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                  {pcTab === 'dashboard' && '📊 区域综合防灾预警中心'}
                  {pcTab === 'gis' && '🗺️ 历史病虫害时空溯源系统'}
                  {pcTab === 'config' && '⚙️ 气象物联与大模型参数中台'}
                </h2>
                <div className="flex items-center gap-6 text-sm">
                  <span className="text-gray-500">更新时间: 2026-06-15 14:30:00</span>
                  <div className="px-4 py-1.5 bg-red-50 text-red-600 rounded-full font-bold flex items-center gap-2 border border-red-100">
                    <AlertTriangle className="w-4 h-4" /> 汛期特殊响应等级：II级
                  </div>
                </div>
              </header>

              <main className="p-8 max-w-[1600px] mx-auto w-full flex-1">
                {pcTab === 'dashboard' && <DashboardTab />}
                {pcTab === 'gis' && <GISView />}
                {pcTab === 'config' && <ConfigView />}
              </main>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}