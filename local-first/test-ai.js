#!/usr/bin/env node

require('dotenv').config();
const AIIntegration = require('./orchestrator/ai-integration');

async function testAI() {
  console.log('🤖 Testing AI Integration...\n');
  
  const ai = new AIIntegration();
  
  try {
    const result = await ai.processQuery('Navigate to YouTube and search for AI tutorials');
    
    console.log('📝 AI Response:');
    console.log('   Intent:', result.intent);
    console.log('   Commands:', result.commands?.length || 0);
    console.log('   Explanation:', result.explanation?.substring(0, 100) + '...');
    
    if (result.intent && result.commands) {
      console.log('\n✅ AI Integration Working!');
    } else {
      console.log('\n❌ AI Integration Issue');
    }
    
  } catch (error) {
    console.error('❌ AI Test Failed:', error.message);
  }
}

testAI();