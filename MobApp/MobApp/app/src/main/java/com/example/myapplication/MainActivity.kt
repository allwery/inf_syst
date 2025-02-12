package com.example.myapplication

import User
import android.content.Intent
import android.os.Bundle
import android.provider.Telephony.Mms.Intents
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.fragment.app.FragmentManager
import androidx.fragment.app.replace
import com.example.myapplication.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var fragmentManager: FragmentManager
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding= ActivityMainBinding.inflate(layoutInflater)
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }





        val linkToAuth=findViewById<TextView>(R.id.linlToAuth)
        val linkToFrag=findViewById<TextView>(R.id.linlToFrag)
        val userLogin=findViewById<EditText>(R.id.userLogin)
        val userPassword=findViewById<EditText>(R.id.userPass)
        val userEmail=findViewById<EditText>(R.id.userEmail)
        val button=findViewById<Button>(R.id.button)
        button.setOnClickListener {
            val login=userLogin.text.toString().trim()
            val pass=userPassword.text.toString().trim()
            val email=userEmail.text.toString().trim()
            if(login=="" ||pass=="" ||email=="" ){
                Toast.makeText(this,"Пусто чет",Toast.LENGTH_LONG).show()
            }
            else{
                val user=User(login,email,pass)
                val db=DBHelper(this,null)
                db.addUser(user)
                Toast.makeText(this,"Добавлен $login",Toast.LENGTH_LONG).show()
                userLogin.text.clear()
                userPassword.text.clear()
                userEmail.text.clear()
            }
        }
        linkToAuth.setOnClickListener{
            val intent=Intent(this,Authorization::class.java)
            startActivity(intent)
        }

        linkToFrag.setOnClickListener{
            val intent=Intent(this,DisplayActivity::class.java)
            startActivity(intent)
        }



    }
}