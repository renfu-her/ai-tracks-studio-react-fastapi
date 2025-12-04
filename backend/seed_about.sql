-- Seed About Us data
-- 添加關於我們的示例數據

USE studio;

-- Insert default About Us content
INSERT INTO about_us (
    title,
    subtitle,
    description,
    image,
    contact_email,
    created_at,
    updated_at
) VALUES (
    'AI-Tracks Studio',
    'Innovative Web & Game Experiences Powered by AI',
    '## Who We Are

AI-Tracks Studio is a creative technology studio dedicated to building innovative web experiences and games. We combine cutting-edge AI technologies with modern web development to create unique, engaging digital experiences.

## Our Mission

Our mission is to push the boundaries of what''s possible on the web. We believe in:

- **Innovation**: Constantly exploring new technologies and approaches
- **Quality**: Delivering polished, professional experiences
- **Creativity**: Combining art and technology in unique ways
- **Accessibility**: Making great experiences available to everyone

## What We Do

We specialize in:

- **Interactive Games**: Browser-based games with modern graphics and engaging gameplay
- **Web Applications**: Responsive, performant web apps that work everywhere
- **AI Integration**: Leveraging AI to create smarter, more dynamic experiences
- **Creative Experiments**: Pushing the boundaries of web technology

## Our Approach

We believe in the power of the web platform. Every project we create is:

- **Fast**: Optimized for performance
- **Beautiful**: Carefully designed with attention to detail
- **Accessible**: Works on all devices and for all users
- **Open**: Built with modern web standards

## Get In Touch

We''re always excited to hear about new projects and collaborations. Whether you have a specific project in mind or just want to chat about web technology, we''d love to hear from you!',
    NULL,
    'contact@ai-tracks.studio',
    NOW(),
    NOW()
);

-- Verify insertion
SELECT id, title, subtitle, contact_email FROM about_us;

