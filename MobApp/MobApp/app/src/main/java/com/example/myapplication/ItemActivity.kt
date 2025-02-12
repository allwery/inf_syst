package com.example.myapplication

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class ItemActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_item)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        val button: Button =findViewById(R.id.button_extend)
        val textView1: TextView =findViewById(R.id.itemTitle)
        val textView2: TextView =findViewById(R.id.itemDescription)
        val textView3: TextView =findViewById(R.id.itemPrice)
        textView1.text=intent.getStringExtra("itemTitle")
        textView2.text=intent.getStringExtra("itemDescription")
        textView3.text=intent.getStringExtra("itemPrice")

    }
}